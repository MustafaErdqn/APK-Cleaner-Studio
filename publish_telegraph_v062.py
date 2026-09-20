"""Publish the prepared v0.6.2 stable changelog to Telegraph."""

from __future__ import annotations

import json
import urllib.parse
from pathlib import Path

from publish_telegraph_v060 import API_ROOT, AUTHOR, AUTHOR_URL, markdown_to_nodes, post_form


ROOT = Path(__file__).resolve().parent
MARKDOWN = ROOT / "TELEGRAPH-CHANGELOG-v0.6.2.md"
ASSET_DIR = ROOT / "release-assets" / "v0.6.2"
PRIVATE_STATE = ROOT / "work" / "telegraph-account-v0.6.2.json"
PUBLIC_RESULT = ROOT / "TELEGRAPH-PUBLISHED-v0.6.2.json"
TITLE = "APK Cleaner Studio v0.6.2 — Kararlı Sürüm Notları"
MEDIA_ROOT = "https://apk-cleaner-release-media.mustafa-erdqn.chatgpt.site/v0.6.2"
IMAGE_NAMES = [
    "home.png",
    "analysis.png",
    "messages-v3.png",
    "installed-app-entry.png",
    "apps-v2.png",
    "apps-actions-v3.png",
    "android-result-actions.png",
    "working-v3.png",
]


def main() -> int:
    image_paths = [ASSET_DIR / name for name in IMAGE_NAMES]
    missing = [path.name for path in image_paths if not path.is_file()]
    if missing:
        raise RuntimeError(f"Eksik sürüm görselleri: {', '.join(missing)}")

    private_state = None
    published = {}
    if PRIVATE_STATE.is_file():
        private_state = json.loads(PRIVATE_STATE.read_text(encoding="utf-8"))
    if PUBLIC_RESULT.is_file():
        published = json.loads(PUBLIC_RESULT.read_text(encoding="utf-8"))
    existing_images = published.get("image_urls", {})
    image_urls = {
        path.name: existing_images.get(path.name)
        or f"{MEDIA_ROOT}/{urllib.parse.quote(path.name)}"
        for path in image_paths
    }
    content = markdown_to_nodes(MARKDOWN.read_text(encoding="utf-8"), image_urls)

    if private_state:
        access_token = private_state["access_token"]
        endpoint = "editPage"
        page_fields = {"path": private_state["page_path"]}
        auth_url = private_state.get("auth_url")
    else:
        account = post_form(
            f"{API_ROOT}/createAccount",
            {"short_name": "apk_repo_grubu", "author_name": AUTHOR, "author_url": AUTHOR_URL},
        )
        access_token = account["access_token"]
        endpoint = "createPage"
        page_fields = {}
        auth_url = account.get("auth_url")

    page = post_form(
        f"{API_ROOT}/{endpoint}",
        {
            **page_fields,
            "access_token": access_token,
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
                "access_token": access_token,
                "auth_url": auth_url,
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
