import hashlib
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

from apply_termux_update import apply


class TermuxUpdaterTests(unittest.TestCase):
    def test_verified_package_is_applied_without_touching_local_jobs(self):
        with tempfile.TemporaryDirectory() as name:
            installation = Path(name)
            update_dir = installation / "studio" / "updates"
            update_dir.mkdir(parents=True)
            jobs = installation / "studio" / "jobs"
            jobs.mkdir()
            (jobs / "keep.txt").write_text("yerel", encoding="utf-8")
            archive = update_dir / "APK-Cleaner-Studio-v0.6.3-Termux.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("VERSION.txt", "APK Cleaner Studio 0.6.3\n")
                package.writestr("start-termux.sh", "#!/bin/bash\n")
                package.writestr("install-termux.sh", "#!/bin/bash\n")
                package.writestr("studio/server.py", "VERSION = '0.6.3'\n")
                package.writestr("studio/updater.py", "# updater\n")
            digest = hashlib.sha256(archive.read_bytes()).hexdigest()
            manifest = installation / ".apk-cleaner-update.json"
            manifest.write_text(json.dumps({"version": "0.6.3", "archive": str(archive), "sha256": digest}), encoding="utf-8")

            self.assertEqual(apply(manifest), "0.6.3")
            self.assertIn("0.6.3", (installation / "VERSION.txt").read_text(encoding="utf-8"))
            self.assertEqual((jobs / "keep.txt").read_text(encoding="utf-8"), "yerel")
            self.assertFalse(manifest.exists())
            self.assertFalse(archive.exists())

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            installation = Path(name)
            update_dir = installation / "studio" / "updates"
            update_dir.mkdir(parents=True)
            archive = update_dir / "APK-Cleaner-Studio-v0.6.3-Termux.zip"
            with zipfile.ZipFile(archive, "w") as package:
                package.writestr("../outside.txt", "hayır")
            manifest = installation / ".apk-cleaner-update.json"
            manifest.write_text(json.dumps({
                "version": "0.6.3",
                "archive": str(archive),
                "sha256": hashlib.sha256(archive.read_bytes()).hexdigest(),
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "güvenli olmayan"):
                apply(manifest)
            self.assertFalse((installation.parent / "outside.txt").exists())


if __name__ == "__main__":
    unittest.main()
