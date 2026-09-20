from __future__ import annotations

import os
import socket
import tempfile
import threading
import time
from pathlib import Path

_thread: threading.Thread | None = None
_lock = threading.Lock()


def _prepare_temp_dir(data_root: str) -> str:
    """Create a private temp directory which Android won't purge as cache."""
    temp_root = Path(data_root).resolve() / "runtime" / "tmp"
    temp_root.mkdir(parents=True, exist_ok=True)

    # Fail at startup with a useful error instead of halfway through an APK job.
    probe = temp_root / f".write-test-{os.getpid()}-{threading.get_ident()}-{time.time_ns()}"
    try:
        with probe.open("xb") as handle:
            handle.write(b"ok")
    finally:
        probe.unlink(missing_ok=True)

    value = str(temp_root)
    for name in ("TMPDIR", "TEMP", "TMP"):
        os.environ[name] = value
    os.environ["APK_CLEANER_TEMP_ROOT"] = value
    # tempfile caches its first successful lookup; replace any stale Chaquopy
    # cache path left behind after Android reclaims the app cache directory.
    tempfile.tempdir = value
    return value


def _wait_until_ready(host: str, port: int, timeout: float = 20.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.25):
                return True
        except OSError:
            time.sleep(0.08)
    return False


def start(data_root: str, port: int = 8765) -> bool:
    """Start the shared APK Cleaner server inside the Android process."""
    global _thread
    with _lock:
        if _thread and _thread.is_alive():
            return _wait_until_ready("127.0.0.1", int(port), 2.0)

        os.environ["APK_CLEANER_ANDROID"] = "1"
        os.environ["APK_CLEANER_DATA_ROOT"] = str(data_root)
        os.environ["HOME"] = str(data_root)
        _prepare_temp_dir(data_root)

        import server

        def run() -> None:
            # start() checks is_alive(); retaining the reference lets stop() join
            # the old listener before another service opens the same port.
            server.serve("127.0.0.1", int(port), False, False, True)

        _thread = threading.Thread(target=run, name="apk-cleaner-http", daemon=True)
        _thread.start()
    return _wait_until_ready("127.0.0.1", int(port))


def stop() -> None:
    global _thread
    with _lock:
        import server
        active = getattr(server, "_ACTIVE_SERVER", None)
        if active is not None:
            active.shutdown()
        server.terminate_active_tools()
        if _thread is not None:
            _thread.join(timeout=5.0)
            if not _thread.is_alive():
                _thread = None
