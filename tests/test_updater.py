import sys
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

from updater import check_for_updates, fetch_remote_update, find_local_update, manifest_url, version_tuple


class UpdaterTests(unittest.TestCase):
    def test_semantic_version_comparison(self):
        self.assertGreater(version_tuple("0.10.0"), version_tuple("0.9.9"))

    def test_newest_local_release_is_selected(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            for version in ("0.3.2", "0.4.1", "0.5.0"):
                (folder / f"APK-Cleaner-Studio-v{version}-Windows.exe").touch()
            (folder / "unrelated.exe").touch()
            update = find_local_update("0.4.0", folder)
            self.assertIsNotNone(update)
            self.assertEqual(update["latest_version"], "0.5.0")
            self.assertEqual(update["source"], "local")

    def test_no_notification_for_current_or_older_files(self):
        with tempfile.TemporaryDirectory() as name:
            folder = Path(name)
            (folder / "APK-Cleaner-Studio-v0.4.0-Windows.exe").touch()
            self.assertIsNone(find_local_update("0.4.0", folder))

    def test_manifest_requires_https(self):
        with mock.patch.dict(os.environ, {"APK_CLEANER_UPDATE_URL": "http://example.test/update.json"}):
            self.assertIsNone(manifest_url())
        with mock.patch.dict(os.environ, {"APK_CLEANER_UPDATE_URL": "https://example.test/update.json"}):
            self.assertEqual(manifest_url(), "https://example.test/update.json")

    def test_remote_update_accepts_only_secure_download_url(self):
        payload = json.dumps({
            "version": "0.6.0",
            "windows_url": "http://example.test/app.exe",
            "notes": "Yeni sürüm",
        }).encode()
        with mock.patch("updater.urllib.request.urlopen", return_value=io.BytesIO(payload)):
            update = fetch_remote_update("0.5.3", "https://example.test/update.json")
        self.assertEqual(update["latest_version"], "0.6.0")
        self.assertIsNone(update["download_url"])

    def test_dev_channel_never_checks_remote_update(self):
        with mock.patch("updater.fetch_remote_update") as remote:
            result = check_for_updates("0.6.0-dev.28")
        remote.assert_not_called()
        self.assertFalse(result["available"])
        self.assertEqual(result["channel"], "dev")


if __name__ == "__main__":
    unittest.main()
