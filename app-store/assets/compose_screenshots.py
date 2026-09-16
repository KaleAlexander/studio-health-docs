#!/usr/bin/env python3
"""Compose App Store screenshots from device captures.

Drop full-resolution portrait captures into source/ and re-run:

    python3 compose_screenshots.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "source"

# Connect slots this app is hitting today. 6.5" is required by the error
# the listing returned; 6.9" is the newer slot if it appears later.
SIZES = {
    "iphone-6.5": (1284, 2778),
    "iphone-6.9": (1320, 2868),
}

GREEN = (47, 66, 56)
CREAM = (243, 238, 230)
CREAM_MUTED = (214, 205, 190)

SHOTS = [
    {
        "src": "01-home.jpg",
        "out": "01-home.png",
        "kicker": "HOME",
        "title": "Your studio.\nToday’s plan.",
    },
    {
        "src": "02-today.jpg",
        "out": "02-today.png",
        "kicker": "TODAY",
        "title": "Log the work\nas you go.",
    },
    {
        "src": "03-calendar.jpg",
        "out": "03-calendar.png",
        "kicker": "CALENDAR",
        "title": "The week\nat a glance.",
    },
    {
        "src": "04-messages.jpg",
        "out": "04-messages.png",
        "kicker": "COACH",
        "title": "Message your\ncoach anytime.",
    },
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, max(size, 8))


def cover(im: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    scale = max(tw / im.width, th / im.height)
    resized = im.resize((round(im.width * scale), round(im.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    cropped = resized.crop((left, top, left + tw, top + th))
    return cropped.filter(ImageFilter.UnsharpMask(radius=1.1, percent=130, threshold=2))


def round_corners(im: Image.Image, radius: int) -> Image.Image:
    rgba = im.convert("RGBA")
    mask = Image.new("L", rgba.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, rgba.width, rgba.height), radius=radius, fill=255)
    rgba.putalpha(mask)
    return rgba


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    canvas_w: int,
    text: str,
    cy: int,
    face: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    spacing: int = 0,
) -> None:
    bbox = draw.multiline_textbbox((0, 0), text, font=face, spacing=spacing, align="center")
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (canvas_w - w) // 2 - bbox[0]
    y = cy - h // 2 - bbox[1]
    draw.multiline_text((x, y), text, font=face, fill=fill, spacing=spacing, align="center")


def compose_framed(src: Image.Image, kicker: str, title: str, canvas_size: tuple[int, int]) -> Image.Image:
    cw, ch = canvas_size
    sx = cw / 1320
    sy = ch / 2868
    canvas = Image.new("RGB", canvas_size, GREEN)
    draw = ImageDraw.Draw(canvas)

    kicker_font = font("/System/Library/Fonts/Supplemental/Georgia.ttf", round(28 * sx))
    title_font = font("/System/Library/Fonts/Supplemental/Didot.ttc", round(92 * sx))

    draw_centered_text(draw, cw, kicker, round(168 * sy), kicker_font, CREAM_MUTED)
    draw_centered_text(draw, cw, title, round(340 * sy), title_font, CREAM, spacing=round(8 * sy))

    shot_w = round(1040 * sx)
    shot_h = round(shot_w * src.height / src.width)
    shot = src.resize((shot_w, shot_h), Image.Resampling.LANCZOS)
    shot = shot.filter(ImageFilter.UnsharpMask(radius=1.1, percent=130, threshold=2))
    radius = round(72 * sx)
    shot = round_corners(shot, radius)

    x = (cw - shot_w) // 2
    y = round(560 * sy)
    shadow = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    shadow_box = Image.new("RGBA", (shot_w, shot_h), (0, 0, 0, 70))
    shadow_box = round_corners(shadow_box, radius)
    shadow.paste(shadow_box, (x, y + round(18 * sy)), shadow_box)
    shadow = shadow.filter(ImageFilter.GaussianBlur(round(22 * sx)))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), shadow)

    canvas.paste(shot, (x, y), shot)
    return canvas.convert("RGB")


def main() -> None:
    for label, size in SIZES.items():
        framed_dir = ROOT / "screenshots" / label
        raw_dir = ROOT / "screenshots" / f"{label}-raw"
        framed_dir.mkdir(parents=True, exist_ok=True)
        raw_dir.mkdir(parents=True, exist_ok=True)

        for spec in SHOTS:
            path = SOURCE / spec["src"]
            if not path.exists():
                raise SystemExit(f"Missing {path}. Put the capture in source/ first.")
            src = Image.open(path).convert("RGB")
            if src.width < 800:
                print(f"warning: {path.name} is {src.width}×{src.height} — replace with a full-res original")

            framed = compose_framed(src, spec["kicker"], spec["title"], size)
            framed.save(framed_dir / spec["out"], "PNG", optimize=True)
            print(f"wrote {framed_dir / spec['out']} {framed.size[0]}×{framed.size[1]}")

            raw = cover(src, size)
            raw.save(raw_dir / spec["out"], "PNG", optimize=True)


if __name__ == "__main__":
    main()
