"""Publish the prepared v0.6.0 changelog to Telegraph.

The generated access token is stored only under work/ so the page can be
edited later without leaking credentials into release artifacts.
"""

from __future__ import annotations

import json
import mimetypes
import os
import re
import secrets
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MARKDOWN = ROOT / "TELEGRAPH-CHANGELOG-v0.6.0.md"
ASSET_DIR = ROOT / "release-assets" / "v0.6.0-review"
PRIVATE_STATE = ROOT / "work" / "telegraph-account-v0.6.0.json"
PUBLIC_RESULT = ROOT / "TELEGRAPH-PUBLISHED-v0.6.0.json"
API_ROOT = "https://api.telegra.ph"
PAGE_ROOT = "https://telegra.ph"
TITLE = "APK Cleaner Studio v0.6.0–v0.6.1 — Kararlı Sürüm Notları"
AUTHOR = "APK Repo Grubu"
AUTHOR_URL = "https://t.me/+WZbVyByWkExjNmZk"
MEDIA_BASE = os.environ.get("TELEGRAPH_MEDIA_BASE", "").rstrip("/")


def post_form(url: str, fields: dict[str, str]) -> dict:
    payload = urllib.parse.urlencode(fields).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=45) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not result.get("ok"):
        raise RuntimeError(f"Telegraph API hatası: {result.get('error', 'Bilinmeyen hata')}")
    return result["result"]


def upload_image(path: Path) -> str:
    if MEDIA_BASE:
        return f"{MEDIA_BASE}/v0.6.0/{urllib.parse.quote(path.name)}"
    boundary = "----APKCleaner" + secrets.token_hex(16)
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode())
    body.extend(
        (
            f'Content-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
            f"Content-Type: {mime}\r\n\r\n"
        ).encode("utf-8")
    )
    body.extend(path.read_bytes())
    body.extend(f"\r\n--{boundary}--\r\n".encode())
    request = urllib.request.Request(
        f"{PAGE_ROOT}/upload",
        data=bytes(body),
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 APK-Cleaner-Studio-Release-Publisher/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        result = json.loads(response.read().decode("utf-8"))
    if not isinstance(result, list) or not result or "src" not in result[0]:
        raise RuntimeError(f"Görsel yüklenemedi: {path.name}")
    src = result[0]["src"]
    return src if src.startswith("http") else PAGE_ROOT + src


INLINE_RE = re.compile(r"(\*\*.+?\*\*|`.+?`|\[[^\]]+\]\([^)]+\))")


def inline_nodes(text: str) -> list[object]:
    nodes: list[object] = []
    cursor = 0
    for match in INLINE_RE.finditer(text):
        if match.start() > cursor:
            nodes.append(text[cursor : match.start()])
        token = match.group(0)
        if token.startswith("**"):
            nodes.append({"tag": "strong", "children": [token[2:-2]]})
        elif token.startswith("`"):
            nodes.append({"tag": "code", "children": [token[1:-1]]})
        else:
            label, url = re.match(r"\[([^\]]+)\]\(([^)]+)\)", token).groups()
            nodes.append({"tag": "a", "attrs": {"href": url}, "children": [label]})
        cursor = match.end()
    if cursor < len(text):
        nodes.append(text[cursor:])
    return nodes or [""]


def markdown_to_nodes(markdown: str, image_urls: dict[str, str]) -> list[dict]:
    lines = markdown.splitlines()
    nodes: list[dict] = []
    paragraph: list[str] = []
    bullet_items: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            if text:
                nodes.append({"tag": "p", "children": inline_nodes(text)})
            paragraph.clear()

    def flush_bullets() -> None:
        if bullet_items:
            nodes.append(
                {
                    "tag": "ul",
                    "children": [
                        {"tag": "li", "children": inline_nodes(item)} for item in bullet_items
                    ],
                }
            )
            bullet_items.clear()

    for index, raw in enumerate(lines):
        line = raw.strip()
        if index == 0 and line.startswith("# "):
            continue
        if not line:
            flush_paragraph()
            flush_bullets()
            continue
        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line)
        if image_match:
            flush_paragraph()
            flush_bullets()
            caption, relative = image_match.groups()
            filename = Path(relative).name
            nodes.append(
                {
                    "tag": "figure",
                    "children": [
                        {"tag": "img", "attrs": {"src": image_urls[filename]}},
                        {"tag": "figcaption", "children": [caption]},
                    ],
                }
            )
        elif line.startswith("#### "):
            flush_paragraph()
            flush_bullets()
            nodes.append({"tag": "h4", "children": [line[5:]]})
        elif line.startswith("## "):
            flush_paragraph()
            flush_bullets()
            nodes.append({"tag": "h3", "children": [line[3:]]})
        elif line.startswith("### "):
            flush_paragraph()
            flush_bullets()
            nodes.append({"tag": "h4", "children": [line[4:]]})
        elif line.startswith("- "):
            flush_paragraph()
            bullet_items.append(line[2:])
        elif line.startswith("— "):
            flush_paragraph()
            flush_bullets()
            nodes.append({"tag": "p", "children": [{"tag": "strong", "children": [line]}]})
        else:
            flush_bullets()
            paragraph.append(line)

    flush_paragraph()
    flush_bullets()
    return nodes


def main() -> int:
    image_names = [
        "01-split-bilesen-secimi-hq.png",
        "02-temizlik-profilleri-ve-iyilestirmeler-hq.png",
        "03-motor-2-ve-yerel-https-hq.png",
        "04-yerel-ag-oturumlari-hq-blur.png",
        "05-islem-gecmisi-hq.png",
    ]
    image_paths = [ASSET_DIR / name for name in image_names]
    missing = [path.name for path in image_paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"Eksik sürüm görselleri: {', '.join(missing)}")

    # Düzenleme sırasında daha önce yayımlanmış görselleri yeniden kullan.
    # Telegraph yükleme uç noktası aynı büyük görselleri tekrar kabul etmeyebilir.
    if PRIVATE_STATE.is_file() and PUBLIC_RESULT.is_file():
        published = json.loads(PUBLIC_RESULT.read_text(encoding="utf-8"))
        existing_images = published.get("image_urls", {})
    else:
        existing_images = {}
    image_urls = {
        path.name: existing_images.get(path.name) or upload_image(path)
        for path in image_paths
    }
    content = markdown_to_nodes(MARKDOWN.read_text(encoding="utf-8"), image_urls)
    if PRIVATE_STATE.is_file():
        private_state = json.loads(PRIVATE_STATE.read_text(encoding="utf-8"))
        account = private_state
        account = {"access_token": private_state["access_token"]}
        endpoint = "editPage"
        page_fields = {"path": private_state["page_path"]}
    else:
        account = post_form(
            f"{API_ROOT}/createAccount",
            {
                "short_name": "apk_repo_grubu",
                "author_name": AUTHOR,
                "author_url": AUTHOR_URL,
            },
        )
        endpoint = "createPage"
        page_fields = {}
    page = post_form(
        f"{API_ROOT}/{endpoint}",
        {
            **page_fields,
            "access_token": account["access_token"],
            "title": TITLE,
            "author_name": AUTHOR,
            "author_url": AUTHOR_URL,
            "content": json.dumps(content, ensure_ascii=False, separators=(",", ":")),
            "return_content": "false",
        },
    )

    PRIVATE_STATE.parent.mkdir(parents=True, exist_ok=True)
    PRIVATE_STATE.write_text(
        json.dumps(
            {
                "access_token": account["access_token"],
                "auth_url": account.get("auth_url", private_state.get("auth_url") if PRIVATE_STATE.is_file() else None),
                "page_path": page["path"],
                "page_url": page["url"],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    PUBLIC_RESULT.write_text(
        json.dumps(
            {
                "title": page["title"],
                "author_name": page["author_name"],
                "path": page["path"],
                "url": page["url"],
                "image_urls": image_urls,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(page["url"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
