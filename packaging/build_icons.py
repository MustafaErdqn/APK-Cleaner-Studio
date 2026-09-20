from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
LOCAL_WEB = ROOT / "studio" / "web"
FONT = Path("C:/Windows/Fonts/arialbd.ttf")


def build_master() -> Image.Image:
    size = 512
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((24, 24, 488, 488), radius=138, fill="#050908")
    draw.rounded_rectangle((48, 48, 464, 464), radius=116, outline="#17221e", width=5)

    font = ImageFont.truetype(str(FONT), 190)
    label = "AC"
    bounds = draw.textbbox((0, 0), label, font=font, stroke_width=1)
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    x = (size - width) / 2
    y = (size - height) / 2 - bounds[1] - 5
    draw.text((x, y), label, font=font, fill="#D9FF43", stroke_width=1, stroke_fill="#D9FF43")
    draw.rounded_rectangle((176, 398, 336, 414), radius=8, fill="#48D5A8")
    return image


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    LOCAL_WEB.mkdir(parents=True, exist_ok=True)
    master = build_master()
    png = PUBLIC / "favicon.png"
    ico = PUBLIC / "favicon.ico"
    master.save(png, format="PNG", optimize=True)
    master.save(ico, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    shutil.copy2(png, LOCAL_WEB / "favicon.png")
    shutil.copy2(ico, LOCAL_WEB / "favicon.ico")


if __name__ == "__main__":
    main()
