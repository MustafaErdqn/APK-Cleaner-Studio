"""Opt-in, read-only resource/geometry regression. Does not render or run Android.

Usage: python tests/verify_dominos_icon.py "path/to/Domino's v8.0.2.apk"
"""
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
AAPT = ROOT / "work/android-toolchain/android-sdk/build-tools/36.0.0/aapt2.exe"


def verify(apk):
    with apk.open("rb") as stream:
        before = hashlib.file_digest(stream, "sha256").hexdigest()

    def dump(kind, *extra):
        return subprocess.check_output([str(AAPT), "dump", kind, str(apk), *extra], encoding="utf-8")

    resources = dump("resources")
    assert "tr.com.dominos" in dump("badging")

    def resource_block(name):
        return re.search(r"resource 0x[0-9a-f]+ " + re.escape(name) + r"\n(.*?)(?=\n    resource|\n  type|\Z)", resources, re.S)[1]

    icon_path = re.search(r"\(anydpi-v26\) \(file\) (\S+)", resource_block("mipmap/ic_launcher"))[1]
    assert "E: adaptive-icon" in dump("xmltree", "--file", icon_path)
    foreground_path = re.search(r"\(file\) (\S+)", resource_block("drawable/ic_launcher_foreground"))[1]
    foreground = dump("xmltree", "--file", foreground_path)
    for edge in ("Left", "Right", "Top", "Bottom"):
        assert re.search(r"inset" + edge + r".*=18\.0+dp", foreground)
    png_path = re.search(r"\(nodpi\) \(file\) (\S+)", resource_block("drawable/ic_launcher_adaptive_fg"))[1]
    with zipfile.ZipFile(apk) as archive:
        header = archive.read(png_path)[:24]
    assert header[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", header[16:24]) == (192, 192)

    # AOSP adaptive layers extend 25% on each side. InsetDrawable's fixed
    # dp padding is converted to density pixels, NOT scaled by setBounds.
    # These calculations explain the defect; they are not device rendering.
    rows = []
    for density in (1, 1.5, 2, 2.625, 3, 4):
        padding = int(18 * density)
        intrinsic_layer = max(round(108 * density), 192 + 2 * padding)
        natural_icon = int(intrinsic_layer / 1.5)
        logical_size = max(72, natural_icon)
        old_content = 72 * 1.5 - 2 * padding
        new_content = (logical_size * 1.5 - 2 * padding) * 72 / logical_size
        assert new_content > 0
        rows.append(dict(density=density, old_foreground_px=old_content, scaled_foreground_px=round(new_content, 2)))
    assert rows[-2]["old_foreground_px"] == 0
    assert rows[-1]["old_foreground_px"] < 0
    with apk.open("rb") as stream:
        assert hashlib.file_digest(stream, "sha256").hexdigest() == before
    print(json.dumps(dict(result="PASS (resource/geometry only)", original_unchanged=True, densities=rows), indent=2))


if __name__ == "__main__":
    verify(Path(sys.argv[1]))
