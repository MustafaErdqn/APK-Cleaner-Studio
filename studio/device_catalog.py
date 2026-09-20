from __future__ import annotations

import json
import re
import threading
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen


CATALOG_URL = "https://storage.googleapis.com/play_public/supported_devices.html"
CATALOG_MAX_BYTES = 12 * 1024 * 1024
CATALOG_REFRESH_SECONDS = 7 * 24 * 60 * 60
ROOT = Path(__file__).resolve().parent
BUNDLED_CATALOG = ROOT / "device-catalog.json"


def _model_key(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().upper()


def _display_name(brand: str, marketing_name: str) -> str:
    brand = re.sub(r"\s+", " ", brand).strip()
    name = re.sub(r"\s+", " ", marketing_name).strip()
    if not name:
        return ""
    if not brand or name.casefold().startswith(brand.casefold()):
        return name
    return f"{brand} {name}"


class _DeviceTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_cell = False
        self.cell_parts: list[str] = []
        self.row: list[str] = []
        self.catalog: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag.lower() == "td":
            self.in_cell = True
            self.cell_parts = []

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        lowered = tag.lower()
        if lowered == "td" and self.in_cell:
            self.row.append("".join(self.cell_parts).strip())
            self.in_cell = False
        elif lowered == "tr":
            if len(self.row) >= 4:
                brand, marketing_name, _device, model = self.row[:4]
                key = _model_key(model)
                name = _display_name(brand, marketing_name)
                if key and name and key not in self.catalog:
                    self.catalog[key] = name
            self.row = []


def parse_catalog_html(document: str) -> dict[str, str]:
    parser = _DeviceTableParser()
    parser.feed(document)
    return parser.catalog


class DeviceCatalog:
    """Resolve Android model codes locally and refresh unknown models in the background."""

    def __init__(self, cache_path: Path) -> None:
        self.cache_path = cache_path
        self._lock = threading.Lock()
        self._refreshing = False
        self._catalog: dict[str, str] = {}
        self._load()

    def _load_file(self, path: Path) -> dict[str, str]:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            models = payload.get("models", payload)
            if isinstance(models, dict):
                return {_model_key(key): str(value) for key, value in models.items() if key and value}
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            pass
        return {}

    def _load(self) -> None:
        bundled = self._load_file(BUNDLED_CATALOG)
        cached = self._load_file(self.cache_path)
        self._catalog = {**bundled, **cached}

    def resolve(self, model: str) -> str | None:
        key = _model_key(model)
        if not key:
            return None
        candidates = [key]
        if "/" in key:
            candidates.append(key.split("/", 1)[0])
        with self._lock:
            for candidate in candidates:
                name = self._catalog.get(candidate)
                if name and _model_key(name) != key:
                    return name
        self.refresh_async()
        return None

    def refresh_async(self, force: bool = False) -> None:
        try:
            fresh = self.cache_path.is_file() and time.time() - self.cache_path.stat().st_mtime < CATALOG_REFRESH_SECONDS
        except OSError:
            fresh = False
        with self._lock:
            if self._refreshing or (fresh and not force):
                return
            self._refreshing = True
        threading.Thread(target=self._refresh, name="device-catalog-refresh", daemon=True).start()

    def _refresh(self) -> None:
        try:
            request = Request(CATALOG_URL, headers={"User-Agent": "APK-Cleaner-Studio/0.6"})
            with urlopen(request, timeout=20) as response:
                final_url = response.geturl() if hasattr(response, "geturl") else CATALOG_URL
                parsed = urlparse(final_url)
                if parsed.scheme != "https" or parsed.hostname != "storage.googleapis.com":
                    return
                declared = int(getattr(response, "headers", {}).get("Content-Length") or 0)
                if declared > CATALOG_MAX_BYTES:
                    return
                raw = response.read(CATALOG_MAX_BYTES + 1)
            if len(raw) > CATALOG_MAX_BYTES:
                return
            catalog = parse_catalog_html(raw.decode("utf-8", errors="replace"))
            if len(catalog) < 1000:
                return
            payload = {"source": CATALOG_URL, "updated_at": int(time.time()), "models": catalog}
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.cache_path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
            temporary.replace(self.cache_path)
            with self._lock:
                self._catalog.update(catalog)
        except (OSError, ValueError):
            pass
        finally:
            with self._lock:
                self._refreshing = False
