import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

import setup_tools


class SetupToolsTests(unittest.TestCase):
    def test_download_streams_and_verifies_sha256_before_replace(self):
        payload = b"tool-payload" * 1000
        with tempfile.TemporaryDirectory() as name:
            target = Path(name) / "tool.jar"
            with mock.patch("setup_tools.urllib.request.urlopen", return_value=io.BytesIO(payload)):
                setup_tools.download("https://example.test/tool.jar", target, hashlib.sha256(payload).hexdigest())
            self.assertEqual(target.read_bytes(), payload)
            self.assertFalse(target.with_suffix(".jar.part").exists())

    def test_download_removes_partial_file_when_checksum_is_wrong(self):
        with tempfile.TemporaryDirectory() as name:
            target = Path(name) / "tool.jar"
            with mock.patch("setup_tools.urllib.request.urlopen", return_value=io.BytesIO(b"broken")):
                with self.assertRaisesRegex(RuntimeError, "SHA-256"):
                    setup_tools.download("https://example.test/tool.jar", target, "0" * 64)
            self.assertFalse(target.exists())
            self.assertFalse(target.with_suffix(".jar.part").exists())

    def test_download_rejects_plain_http_before_network_access(self):
        with tempfile.TemporaryDirectory() as name, mock.patch("setup_tools.urllib.request.urlopen") as open_url:
            with self.assertRaisesRegex(RuntimeError, "HTTPS"):
                setup_tools.download("http://example.test/tool.jar", Path(name) / "tool.jar")
        open_url.assert_not_called()

    def test_runtime_zip_extraction_rejects_path_traversal(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            archive = root / "runtime.zip"
            destination = root / "out"
            destination.mkdir()
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("../outside.txt", b"escaped")
            with self.assertRaisesRegex(RuntimeError, "güvenli olmayan|dışına"):
                setup_tools._safe_unpack_archive(archive, destination)
            self.assertFalse((root / "outside.txt").exists())

    def test_runtime_zip_extraction_keeps_files_inside_destination(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            archive = root / "runtime.zip"
            destination = root / "out"
            destination.mkdir()
            with zipfile.ZipFile(archive, "w") as output:
                output.writestr("jdk/bin/java", b"runtime")
            setup_tools._safe_unpack_archive(archive, destination)
            self.assertEqual((destination / "jdk" / "bin" / "java").read_bytes(), b"runtime")

    def test_install_is_noop_when_bundled_toolchain_is_complete(self):
        status = {"fully_ready": True, "zipalign": True}
        tools = mock.Mock(java="java", apkeditor=Path("APKEditor.jar"), uber_signer=Path("signer.jar"), zipalign="zipalign")
        tools.status.return_value = status
        with mock.patch("setup_tools.Toolchain.detect", return_value=tools), mock.patch("setup_tools.download") as download:
            result = setup_tools.install()
        download.assert_not_called()
        self.assertTrue(result["ready"])
        self.assertEqual(result["installed"], [])
        self.assertEqual(result["errors"], [])

    def test_termux_java_prefers_openjdk_25(self):
        completed = mock.Mock(returncode=0, stdout="ok")
        with mock.patch.dict("setup_tools.os.environ", {"PREFIX": "/data/data/com.termux/files/usr"}), mock.patch(
            "setup_tools.subprocess.run", return_value=completed
        ) as run:
            self.assertEqual(setup_tools.install_portable_java(), "openjdk-25")
        run.assert_called_once_with(
            ["pkg", "install", "-y", "openjdk-25"],
            text=True,
            stdout=setup_tools.subprocess.PIPE,
            stderr=setup_tools.subprocess.STDOUT,
        )

    def test_termux_java_falls_back_to_openjdk_21(self):
        failed = mock.Mock(returncode=1, stdout="not available")
        completed = mock.Mock(returncode=0, stdout="ok")
        with mock.patch.dict("setup_tools.os.environ", {"PREFIX": "/data/data/com.termux/files/usr"}), mock.patch(
            "setup_tools.subprocess.run", side_effect=[failed, completed]
        ) as run:
            self.assertEqual(setup_tools.install_portable_java(), "openjdk-21")
        self.assertEqual(run.call_args_list[0].args[0][-1], "openjdk-25")
        self.assertEqual(run.call_args_list[1].args[0][-1], "openjdk-21")


if __name__ == "__main__":
    unittest.main()
