from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from engine import DATA_ROOT, ROOT

RELEASE_NAME = re.compile(r"^APK-Cleaner-(?:Studio|Manager)-v(?P<version>\d+\.\d+\.\d+)-Windows\.exe$", re.IGNORECASE)
USER_AGENT = "APK-Cleaner-Studio-Updater/1.0"
MAX_MANIFEST_BYTES = 256 * 1024


def version_tuple(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value.strip())
    if not match:
        raise ValueError("Geçersiz sürüm numarası.")
    return tuple(int(part) for part in match.groups())


def _channel_config() -> dict:
    for path in (DATA_ROOT / "update-channel.json", ROOT / "update-channel.json"):
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            continue
    return {}


def manifest_url() -> str | None:
    value = os.environ.get("APK_CLEANER_UPDATE_URL") or _channel_config().get("manifest_url")
    if not value:
        return None
    parsed = urllib.parse.urlparse(str(value))
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    return str(value)


def find_local_update(current_version: str, search_dir: Path | None = None) -> dict | None:
    if search_dir is None:
        if not (getattr(sys, "frozen", False) and os.name == "nt"):
            return None
        search_dir = Path(sys.executable).resolve().parent
    current = version_tuple(current_version)
    candidates: list[tuple[tuple[int, int, int], str, Path]] = []
    release_files = {
        *search_dir.glob("APK-Cleaner-Studio-v*-Windows.exe"),
        *search_dir.glob("APK-Cleaner-Manager-v*-Windows.exe"),
    }
    for path in release_files:
        match = RELEASE_NAME.fullmatch(path.name)
        if not match:
            continue
        version = match.group("version")
        parsed = version_tuple(version)
        if parsed > current:
            candidates.append((parsed, version, path))
    if not candidates:
        return None
    _, version, path = max(candidates, key=lambda item: item[0])
    return {
        "available": True,
        "latest_version": version,
        "source": "local",
        "filename": path.name,
        "notes": "Yeni sürüm uygulama klasöründe hazır. Mevcut sürümü kapatıp yeni EXE dosyasını açabilirsin.",
        "download_url": None,
    }


def fetch_remote_update(current_version: str, url: str) -> dict | None:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=6) as response:
        final_url = urllib.parse.urlparse(response.geturl() if hasattr(response, "geturl") else url)
        if final_url.scheme != "https" or not final_url.netloc:
            raise ValueError("Güncelleme bildirimi güvenli olmayan bir adrese yönlendirildi.")
        headers = getattr(response, "headers", {})
        declared = int(headers.get("Content-Length") or 0)
        if declared > MAX_MANIFEST_BYTES:
            raise ValueError("Güncelleme bildirimi boyut sınırını aşıyor.")
        raw = response.read(MAX_MANIFEST_BYTES + 1)
        if len(raw) > MAX_MANIFEST_BYTES:
            raise ValueError("Güncelleme bildirimi boyut sınırını aşıyor.")
        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Güncelleme bildirimi nesne biçiminde değil.")
    latest = str(payload.get("version", ""))
    if version_tuple(latest) <= version_tuple(current_version):
        return None
    if os.environ.get("APK_CLEANER_ANDROID") == "1":
        platform_url = payload.get("android_url")
    else:
        platform_url = payload.get("windows_url") if os.name == "nt" else payload.get("termux_url")
    download_url = platform_url or payload.get("download_url")
    if download_url and urllib.parse.urlparse(str(download_url)).scheme != "https":
        download_url = None
    return {
        "available": True,
        "latest_version": latest,
        "source": "remote",
        "filename": payload.get("filename"),
        "notes": str(payload.get("notes") or "Yeni APK Cleaner Studio sürümü kullanıma hazır."),
        "published_at": payload.get("published_at"),
        "download_url": download_url,
        "sha256": payload.get("sha256"),
    }


def check_for_updates(current_version: str) -> dict:
    if "-dev." in current_version:
        return {
            "current_version": current_version,
            "available": False,
            "configured": False,
            "update": None,
            "warning": None,
            "channel": "dev",
        }
    local = find_local_update(current_version)
    url = manifest_url()
    remote = None
    warning = None
    if url:
        try:
            remote = fetch_remote_update(current_version, url)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            warning = f"Güncelleme kanalı şu anda kontrol edilemedi: {exc}"
    updates = [item for item in (local, remote) if item]
    selected = max(updates, key=lambda item: version_tuple(item["latest_version"])) if updates else None
    return {
        "current_version": current_version,
        "available": bool(selected),
        "configured": bool(url),
        "update": selected,
        "warning": warning,
    }
