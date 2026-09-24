from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

MAX_ARCHIVE_ENTRIES = 20_000
MAX_EXPANDED_BYTES = 2 * 1024 * 1024 * 1024


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(name: str) -> PurePosixPath:
    value = PurePosixPath(name)
    if value.is_absolute() or not value.parts or any(part in {"", ".", ".."} for part in value.parts):
        raise ValueError("Güncelleme arşivinde güvenli olmayan bir dosya yolu bulundu.")
    return value


def apply(manifest_path: Path) -> str:
    installation = manifest_path.resolve().parent
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    archive = Path(str(payload.get("archive") or "")).resolve()
    expected = str(payload.get("sha256") or "").lower()
    update_root = (installation / "studio" / "updates").resolve()
    if update_root not in archive.parents or archive.suffix.lower() != ".zip":
        raise ValueError("Güncelleme arşivi beklenen güvenli klasörde değil.")
    if not archive.is_file() or len(expected) != 64 or sha256(archive) != expected:
        raise ValueError("Termux güncellemesinin SHA-256 doğrulaması başarısız oldu.")

    temporary = Path(tempfile.mkdtemp(prefix=".apk-cleaner-update-", dir=installation))
    try:
        with zipfile.ZipFile(archive) as package:
            members = package.infolist()
            if len(members) > MAX_ARCHIVE_ENTRIES:
                raise ValueError("Güncelleme arşivi çok fazla dosya içeriyor.")
            if sum(item.file_size for item in members) > MAX_EXPANDED_BYTES:
                raise ValueError("Güncelleme arşivinin açılmış boyutu güvenli sınırı aşıyor.")
            for item in members:
                relative = safe_member(item.filename)
                mode = item.external_attr >> 16
                if stat.S_ISLNK(mode):
                    raise ValueError("Güncelleme arşivinde sembolik bağlantıya izin verilmez.")
                destination = temporary.joinpath(*relative.parts)
                destination.parent.mkdir(parents=True, exist_ok=True)
                if item.is_dir():
                    destination.mkdir(parents=True, exist_ok=True)
                    continue
                with package.open(item) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output, 1024 * 1024)

        for required in ("VERSION.txt", "start-termux.sh", "studio/server.py", "studio/updater.py"):
            if not (temporary / required).is_file():
                raise ValueError(f"Güncelleme paketi gerekli {required} dosyasını içermiyor.")

        for source in sorted(temporary.rglob("*")):
            relative = source.relative_to(temporary)
            destination = installation / relative
            if source.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            replacement = destination.with_name(destination.name + ".update-part")
            shutil.copy2(source, replacement)
            os.replace(replacement, destination)

        os.chmod(installation / "start-termux.sh", 0o755)
        os.chmod(installation / "install-termux.sh", 0o755)
        version = str(payload.get("version") or "yeni")
        archive.unlink(missing_ok=True)
        manifest_path.unlink(missing_ok=True)
        return version
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Kullanım: apply_termux_update.py <manifest>")
    try:
        updated = apply(Path(sys.argv[1]))
        print(f"APK Cleaner Studio v{updated} doğrulandı ve kuruldu.", flush=True)
    except Exception as error:
        print(f"Güncelleme uygulanamadı: {error}", file=sys.stderr, flush=True)
        raise SystemExit(1) from None
