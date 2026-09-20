"""Opt-in real multidex regression. Does not execute or overwrite the input APK."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from studio.engine import inspect_startup_calls


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify(apk):
    original_hash = digest(apk)
    candidates = inspect_startup_calls(apk)
    expected = {("Lcom/android/meta/ads;", "facebook", "Diyalog"),
                ("Lcom/android/meta/adstst;", "Start", "Toast")}
    selected = [row for row in candidates if row["owner_class"] == "Lcom/lmr/lfm/MainActivity;"
                and row["owner_method"] == "onResume"
                and (row["target_class"], row["target_method"], row["kind"]) in expected]
    assert {(r["target_class"], r["target_method"], r["kind"]) for r in selected} == expected
    assert {r["dex"] for r in selected} == {"classes7.dex"}
    assert {r["id"] for r in candidates if r.get("focus") == "priority"} == {r["id"] for r in selected}
    cp = os.pathsep.join(str(ROOT / "studio/tools" / name)
                         for name in ("direct-dex-patcher.jar", "dexlib2-runtime.jar"))
    with tempfile.TemporaryDirectory(prefix="verify-myt-") as folder, zipfile.ZipFile(apk) as archive:
        work = Path(folder)
        original = archive.read("classes7.dex")
        source, output = work / "input.dex", work / "patched.dex"
        source.write_bytes(original)
        cmd = [shutil.which("java"), "-cp", cp, "local.apkcleaner.dex.DirectDexPatcher",
               "--input", str(source), "--output", str(output)]
        for row in selected:
            cmd.extend(("--startup-target", row["id"].split(":", 1)[1]))
        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", timeout=60)
        assert result.returncode == 0, result.stderr
        assert "message_patches=2" in result.stdout, result.stdout
        patched = output.read_bytes()
        assert len(patched) == len(original)
        offsets = [i for i in range(32, len(original)) if original[i] != patched[i]]
        assert 0 < len(offsets) <= 12
        assert all(patched[i] == 0 for i in offsets)
        assert patched[12:32] == hashlib.sha1(patched[32:]).digest()
        assert struct.unpack_from("<I", patched, 8)[0] == zlib.adler32(patched[12:]) & 0xffffffff
        inspection = work / "inspection-only.apk"
        # Only DEX entries are needed for re-scanning, never a distributable APK.
        with zipfile.ZipFile(inspection, "w") as target:
            for entry in archive.infolist():
                if entry.filename.endswith(".dex"):
                    target.writestr(entry.filename, patched if entry.filename == "classes7.dex"
                                    else archive.read(entry))
        remaining = inspect_startup_calls(inspection)
        assert {r["id"] for r in remaining} == {r["id"] for r in candidates} - {r["id"] for r in selected}
    assert digest(apk) == original_hash
    return {"source_unchanged": True, "priority_candidates": len(selected), "candidates_before": len(candidates),
            "selected_roots_removed": len(selected), "candidates_after": len(remaining),
            "other_candidates_preserved": True, "changed_dex_bytes_excluding_header": len(offsets)}


if __name__ == "__main__":
    print(json.dumps(verify(Path(sys.argv[1])), indent=2))
