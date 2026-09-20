"""Full HTTP upload -> analyze -> patch -> poll -> download -> delete audit."""

from __future__ import annotations

import io
import json
import socket
import subprocess
import sys
import time
import urllib.request
import urllib.error
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLIENT_ID = "b" * 24


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def request(url: str, *, method: str = "GET", body: bytes | None = None, headers: dict | None = None) -> tuple[int, bytes]:
    merged = {"X-Client-ID": CLIENT_ID, **(headers or {})}
    req = urllib.request.Request(url, data=body, method=method, headers=merged)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def main() -> int:
    candidates = sorted((ROOT / "studio" / "jobs").glob("*/hello-with-ad-call.apk"))
    fixture = candidates[0] if candidates else ROOT / "work" / "hello-with-ad-call.apk"
    if not fixture.is_file():
        raise RuntimeError("HTTP akışı için kalıcı hello-with-ad-call.apk test örneği bulunamadı.")
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    process = subprocess.Popen(
        [sys.executable, str(ROOT / "studio" / "server.py"), "--host", "127.0.0.1", "--port", str(port), "--no-open", "--no-trust-prompt"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    job_id = None
    started = time.perf_counter()
    try:
        deadline = time.monotonic() + 20
        while True:
            try:
                request(base + "/api/status")
                break
            except Exception:
                if process.poll() is not None:
                    raise RuntimeError(process.stdout.read() if process.stdout else "Sunucu erken kapandı.")
                if time.monotonic() > deadline:
                    raise RuntimeError("HTTP iş akışı sunucusu hazır olmadı.")
                time.sleep(0.1)

        boundary = "----APKCleanerAudit" + uuid.uuid4().hex
        filename = "stability-http-audit.apk"
        payload = (
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"package\"; filename=\"{filename}\"\r\n"
            "Content-Type: application/vnd.android.package-archive\r\n\r\n"
        ).encode() + fixture.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
        upload_mark = time.perf_counter()
        status, raw = request(
            base + "/api/analyze",
            method="POST",
            body=payload,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}", "Content-Length": str(len(payload))},
        )
        upload_seconds = time.perf_counter() - upload_mark
        upload = json.loads(raw)
        if status != 200:
            raise RuntimeError(f"Yükleme/analiz isteği reddedildi: {upload}")
        job_id = upload["job_id"]
        if status != 200 or upload["analysis"]["network_count"] != 1:
            raise RuntimeError(f"Yükleme/analiz yanıtı geçersiz: {upload}")

        clean_payload = json.dumps({
            "job_id": job_id,
            "profile": "safe",
            "operation": "patch",
            "patch_ads": True,
            "strip_debug": False,
            "optimize_apk": False,
            "deobfuscate_resources": False,
            "normalize_resources": False,
        }).encode()
        status, raw = request(base + "/api/clean", method="POST", body=clean_payload, headers={"Content-Type": "application/json"})
        accepted = json.loads(raw)
        if status not in {200, 202} or accepted["job_id"] != job_id:
            raise RuntimeError(f"İş kabul yanıtı geçersiz: {accepted}")

        deadline = time.monotonic() + 90
        states = []
        while True:
            _, raw = request(base + f"/api/jobs/{job_id}/state")
            state = json.loads(raw)
            states.append((state.get("status"), state.get("progress", 0)))
            if state.get("status") == "done":
                break
            if state.get("status") == "error":
                raise RuntimeError(state.get("message", "Motor işi hata verdi."))
            if time.monotonic() > deadline:
                raise RuntimeError(f"HTTP motor işi zaman aşımına uğradı. Son durumlar: {states[-20:]}")
            time.sleep(0.1)
        progresses = [value for _status, value in states]
        if any(later < earlier for earlier, later in zip(progresses, progresses[1:])) or progresses[-1] != 100:
            raise RuntimeError(f"Durum ilerlemesi tutarsız: {progresses}")

        _, apk_bytes = request(base + f"/api/jobs/{job_id}/download")
        with zipfile.ZipFile(io.BytesIO(apk_bytes)) as archive:
            if archive.testzip() is not None or not any(name.startswith("META-INF/") for name in archive.namelist()):
                raise RuntimeError("HTTP indirme çıktısı geçerli imzalı APK değil.")
        _, report_bytes = request(base + f"/api/jobs/{job_id}/report")
        if filename.encode() not in report_bytes:
            raise RuntimeError("İşlem raporu kaynak dosya adını içermiyor.")
        _, history_raw = request(base + "/api/history")
        history = json.loads(history_raw)
        if not any(row["job_id"] == job_id and row["has_output"] for row in history["jobs"]):
            raise RuntimeError("Tamamlanan iş geçmişte görünmedi.")

        _, delete_raw = request(base + f"/api/jobs/{job_id}/delete", method="POST", body=b"")
        deleted = json.loads(delete_raw)
        if not deleted.get("ok") or (ROOT / "studio" / "jobs" / job_id).exists():
            raise RuntimeError("HTTP geçmiş silme işi yerel dosyaları kaldırmadı.")
        job_id = None
        print(json.dumps({
            "upload_bytes": fixture.stat().st_size,
            "upload_and_analysis_seconds": round(upload_seconds, 3),
            "accepted_status": status,
            "poll_samples": len(states),
            "download_bytes": len(apk_bytes),
            "history_visible": True,
            "delete_complete": True,
            "workflow_seconds": round(time.perf_counter() - started, 2),
        }, ensure_ascii=False, indent=2))
    finally:
        if job_id:
            candidate = ROOT / "studio" / "jobs" / job_id
            if candidate.is_dir() and candidate.parent == ROOT / "studio" / "jobs":
                import shutil
                shutil.rmtree(candidate)
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
