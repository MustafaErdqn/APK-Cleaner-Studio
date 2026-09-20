"""Black-box abuse tests for the local HTTP API and untrusted package boundary."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
import uuid
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROXY_HOST = "studio-test.keenetic.link"


def free_port() -> int:
    with socket.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        return int(probe.getsockname()[1])


def request(url: str, *, method: str = "GET", body: bytes | None = None, headers: dict[str, str] | None = None):
    candidate = urllib.request.Request(url, data=body, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(candidate, timeout=20) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()
    except urllib.error.URLError:
        return 0, {}, b""


def proxy_headers(address: str, client_id: str, *, origin: str | None = None) -> dict[str, str]:
    result = {
        "Host": PROXY_HOST,
        "X-Forwarded-Host": PROXY_HOST,
        "X-Forwarded-Proto": "https",
        "X-Forwarded-For": address,
        "X-Client-ID": client_id,
    }
    if origin is not None:
        result["Origin"] = origin
    return result


def multipart(filename: str, payload: bytes) -> tuple[bytes, str]:
    boundary = "----security-" + uuid.uuid4().hex
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="package"; filename="{filename}"\r\n'
        "Content-Type: application/vnd.android.package-archive\r\n\r\n"
    ).encode() + payload + f"\r\n--{boundary}--\r\n".encode()
    return body, f"multipart/form-data; boundary={boundary}"


def main() -> int:
    port = free_port()
    base = f"http://127.0.0.1:{port}"
    owner = proxy_headers("1.1.1.1", "security-owner-123", origin=f"https://{PROXY_HOST}")
    attacker = proxy_headers("8.8.8.8", "security-attacker-123", origin=f"https://{PROXY_HOST}")
    findings: list[str] = []

    with tempfile.TemporaryDirectory(prefix="apk-cleaner-security-audit-") as data_name:
        environment = os.environ.copy()
        environment["APK_CLEANER_DATA_ROOT"] = data_name
        environment["APK_CLEANER_TRUSTED_PROXY"] = "127.0.0.1"
        process = subprocess.Popen(
            [sys.executable, str(ROOT / "studio" / "server.py"), "--host", "127.0.0.1", "--port", str(port), "--no-open", "--no-trust-prompt", "--prefer-http"],
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        try:
            deadline = time.monotonic() + 25
            while time.monotonic() < deadline:
                status, _headers, _payload = request(base + "/api/status", headers=owner)
                if status == 200:
                    break
                time.sleep(0.1)
            else:
                raise RuntimeError("Güvenlik test sunucusu başlamadı.")

            status, headers, _ = request(base + "/", headers=owner)
            assert status == 200
            policy = headers.get("Content-Security-Policy", "")
            assert "frame-ancestors 'none'" in policy and "object-src 'none'" in policy
            assert "'unsafe-inline'" not in policy
            assert headers.get("X-Frame-Options") == "DENY"
            assert headers.get("Cache-Control") == "no-store"

            foreign = proxy_headers("1.1.1.1", "security-owner-123", origin="https://evil.example")
            status, _, _ = request(base + "/api/client", method="POST", body=b"{}", headers={**foreign, "Content-Type": "application/json"})
            assert status == 403
            status, _, _ = request(base + "/api/status", headers={"Host": "evil.example"})
            assert status == 403
            for path in ("/%2e%2e/server.py", "/..%2f..%2fandroid/signing.properties", "/%2e%2e%5csecret"):
                status, _, _ = request(base + path, headers=owner)
                assert status in {403, 404}, (path, status)

            status, _, _ = request(base + "/api/setup", method="POST", headers=owner)
            assert status == 403

            fixture = ROOT / "work" / "hello-with-ad-call.apk"
            payload = fixture.read_bytes()
            body, content_type = multipart("owner.apk", payload)
            status, _, raw = request(base + "/api/analyze", method="POST", body=body, headers={**owner, "Content-Type": content_type})
            assert status == 200, raw[:300]
            job_id = json.loads(raw)["job_id"]

            for action in ("state", "report", "download"):
                status, _, _ = request(base + f"/api/jobs/{job_id}/{action}", headers=attacker)
                assert status == 403, (action, status)
            status, _, _ = request(base + f"/api/jobs/{job_id}/reuse", method="POST", headers=attacker)
            assert status == 403
            status, _, _ = request(base + f"/api/jobs/{job_id}/reuse", headers=owner)
            assert status == 404

            bomb_path = Path(data_name) / "bomb.apk"
            with zipfile.ZipFile(bomb_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
                archive.writestr("classes.dex", b"0" * (2 * 1024 * 1024))
            body, content_type = multipart("bomb.apk", bomb_path.read_bytes())
            status, _, raw = request(base + "/api/analyze", method="POST", body=body, headers={**owner, "Content-Type": content_type})
            assert status == 400 and "sıkıştırma oranı" in raw.decode("utf-8")
            job_dirs = [path for path in (Path(data_name) / "jobs").iterdir() if path.is_dir()]
            assert len(job_dirs) == 1, "Reddedilen arşiv çalışma verisi bıraktı."

            findings.extend([
                "same-origin mutation enforcement",
                "host-header rejection",
                "static path traversal rejection",
                "remote setup denial",
                "cross-client job isolation",
                "GET mutation rejection",
                "decompression-bomb rejection and cleanup",
                "CSP/frame/cache security headers",
            ])
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait(timeout=5)

    print(json.dumps({"passed": len(findings), "checks": findings}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
