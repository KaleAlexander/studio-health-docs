#!/usr/bin/env python3
"""Instagram stories, 1080×1920. Solid ground, a headline sticker, a smaller app shot.

Each frame is its own ad. Leave the bottom for the Get started for free sticker.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ig_render", ROOT / "render.py")
ig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ig)

OUT = ROOT / "stories"
SHOTS = Path(
    "/Users/kalehanby/Documents/GitHub/studio-health-docs/app-store/assets/screenshots/iphone-6.9"
)
W, H = 1080, 1920

INK = (22, 20, 18, 255)
PAPER = (255, 251, 245, 255)
ACCENT = (196, 92, 38, 255)
WHITE = (255, 255, 255, 255)


def solid(color) -> Image.Image:
    return Image.new("RGBA", (W, H), color + (255,))


def app_shot(name: str, top: int, width: int, inner_top: int = 0, radius: int = 0) -> Image.Image:
    """The phone, lifted off the marketing frame, at story size."""
    src = Image.open(SHOTS / name).convert("RGB")
    sub = src.crop((0, top, src.width, src.height))
    rgba = ig.chroma(sub, ig.PHONE_BG, cutoff=8, gain=12)
    bbox = rgba.getchannel("A").point(lambda p: 255 if p > 18 else 0).getbbox()
    phone = rgba.crop(bbox)
    if inner_top:
        phone = phone.crop((0, inner_top, phone.width, phone.height))
    phone = ig.scale_w(phone, width)
    if radius:
        mask = Image.new("L", phone.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, phone.width - 1, phone.height - 1), radius=radius, fill=255)
        phone.putalpha(mask)
    return phone


def shadowed(im: Image.Image, angle: float) -> Image.Image:
    tilted = im.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)
    shadow = Image.new("RGBA", tilted.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).bitmap((0, 0), tilted.getchannel("A"), fill=(0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    frame = Image.new("RGBA", (tilted.width + 64, tilted.height + 72), (0, 0, 0, 0))
    frame.alpha_composite(shadow, (32, 44))
    frame.alpha_composite(tilted, (32, 28))
    return frame


def sticker(lines, font, fg, bg, angle, pad=(20, 11), gap=5, radius=12, ragged=True):
    """One Instagram text block: a box behind each line, then tilted."""
    widths = []
    inks = []
    for line in lines:
        box = font.getbbox(line)
        widths.append(font.getlength(line) + pad[0] * 2)
        inks.append(box[1])
    if not ragged:
        widths = [max(widths)] * len(widths)
    text_h = max(font.getbbox(line)[3] - font.getbbox(line)[1] for line in lines)
    box_h = text_h + pad[1] * 2
    total_h = len(lines) * box_h + (len(lines) - 1) * gap
    total_w = max(widths)
    plate = Image.new("RGBA", (int(total_w) + 8, int(total_h) + 8), (0, 0, 0, 0))
    draw = ImageDraw.Draw(plate)
    y = 0
    for line, width, top in zip(lines, widths, inks):
        draw.rounded_rectangle((0, y, width, y + box_h), radius=radius, fill=bg)
        draw.text((pad[0], y + pad[1] - top), line, font=font, fill=fg)
        y += box_h + gap
    shadow = Image.new("RGBA", plate.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).bitmap((0, 0), plate.getchannel("A"), fill=(0, 0, 0, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    frame = Image.new(
        "RGBA",
        (plate.width + 48, plate.height + 48),
        (0, 0, 0, 0),
    )
    frame.alpha_composite(shadow, (24, 30))
    frame.alpha_composite(plate, (24, 22))
    return frame.rotate(angle, resample=Image.Resampling.BICUBIC, expand=True)


def paste(base, im, xy):
    x, y = xy
    if x < 0 or y < 0:
        im = im.crop((max(0, -x), max(0, -y), im.width, im.height))
        x, y = max(0, x), max(0, y)
    im = im.crop((0, 0, min(im.width, base.width - x), min(im.height, base.height - y)))
    if im.width <= 0 or im.height <= 0:
        return
    base.alpha_composite(im, (x, y))


def frame(
    hook,
    body,
    aside,
    shot,
    phone_at,
    phone_angle,
    *,
    body_at=(64, 530),
    aside_at=(48, 1180),
    hook_angle=-3.2,
    body_angle=1.8,
    phone_w=500,
    inner_top=0,
    radius=0,
):
    im = solid(ig.FOREST)
    paste(
        im,
        sticker(hook, ig.sans(54, 720), INK, PAPER, hook_angle),
        (48, 250),
    )
    paste(
        im,
        sticker(body, ig.sans(38, 640), WHITE, (24, 22, 20, 235), body_angle),
        body_at,
    )
    paste(
        im,
        shadowed(app_shot(shot, 470, phone_w, inner_top, radius), phone_angle),
        phone_at,
    )
    if aside:
        paste(
            im,
            sticker(aside, ig.sans(32, 680), PAPER, ACCENT, -7),
            aside_at,
        )
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [
        (
            "01-trained.png",
            frame(
                ["ai that's trained", "on your programs."],
                [
                    "describe what they need.",
                    "it drafts in your style.",
                    "sets, cues, and the video.",
                ],
                ["they open it and just train."],
                "02-today.png",
                (530, 1040),
                -7,
            ),
        ),
        (
            "02-build-app.png",
            frame(
                ["build your own app."],
                [
                    "your name. your colours.",
                    "turn off anything you don't run.",
                    "they train in your studio.",
                ],
                None,
                "01-home.png",
                (500, 980),
                6,
                body_at=(64, 470),
                phone_w=520,
                inner_top=280,
                radius=44,
                hook_angle=2.2,
                body_angle=-1.5,
            ),
        ),
        (
            "03-sounds-like-you.png",
            frame(
                ["the next draft", "sounds like you."],
                [
                    "trained on how you coach.",
                    "and the programs you write.",
                    "not a blank page.",
                ],
                ["your library. your voice."],
                "02-today.png",
                (540, 1060),
                -5,
                hook_angle=-2.4,
                body_angle=2.1,
            ),
        ),
        (
            "04-just-train.png",
            frame(
                ["they open it", "and just train."],
                [
                    "today's work is on their phone.",
                    "sets, the cue, the video.",
                    "your studio. their pocket.",
                ],
                None,
                "02-today.png",
                (510, 1020),
                5,
                body_at=(72, 500),
                hook_angle=2.6,
                body_angle=-1.8,
            ),
        ),
    ]
    cell_w = 240
    cell_h = round(cell_w * H / W)
    gap = 16
    pad = 24
    board = Image.new(
        "RGB",
        (pad * 2 + len(slides) * cell_w + (len(slides) - 1) * gap, cell_h + pad * 2),
        (255, 255, 255),
    )
    for i, (name, im) in enumerate(slides):
        path = OUT / name
        ig.finish(im).save(path, "PNG", optimize=True)
        print(path)
        tile = im.convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        board.paste(tile, (pad + i * (cell_w + gap), pad))
    for old_name in ("01-sunday.png", "02-open-it.png", "02-their-app.png"):
        old = OUT / old_name
        if old.exists():
            old.unlink()
    preview = ROOT / "story-preview.png"
    board.save(preview, "PNG", optimize=True)
    print(preview)


if __name__ == "__main__":
    main()
