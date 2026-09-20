import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "studio"))

from device_catalog import DeviceCatalog, parse_catalog_html


class DeviceCatalogTests(unittest.TestCase):
    def test_official_table_shape_is_parsed(self):
        document = """<table><tr><th>Retail Branding</th></tr><tr><td>Samsung</td><td>Galaxy S24 Ultra</td><td>e3q</td><td>SM-S928B</td></tr></table>"""
        self.assertEqual(parse_catalog_html(document)["SM-S928B"], "Samsung Galaxy S24 Ultra")

    def test_bundled_catalog_resolves_model_variants_offline(self):
        with tempfile.TemporaryDirectory() as name:
            catalog = DeviceCatalog(Path(name) / "cache.json")
            self.assertEqual(catalog.resolve("SM-S928B"), "Samsung Galaxy S24 Ultra")
            self.assertEqual(catalog.resolve("SM-S928B/DS"), "Samsung Galaxy S24 Ultra")

    def test_refresh_rejects_https_redirect_to_untrusted_host(self):
        with tempfile.TemporaryDirectory() as name:
            cache = Path(name) / "cache.json"
            catalog = DeviceCatalog(cache)
            response = io.BytesIO(b"<table></table>")
            response.geturl = lambda: "https://evil.example/catalog.html"
            response.headers = {}
            with mock.patch("device_catalog.urlopen", return_value=response):
                catalog._refresh()
            self.assertFalse(cache.exists())


if __name__ == "__main__":
    unittest.main()
