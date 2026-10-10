#!/usr/bin/env python3
"""Pinned how-it-works carousel. 1080×1350, upload 01 through 06 in order."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ig_render", ROOT / "render.py")
ig = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ig)

OUT = ROOT / "carousel"
W, H = 1080, 1350
M = 88

FOREST, PAPER, INK, MUTED, ACCENT = ig.FOREST, ig.PAPER, ig.INK, ig.MUTED, ig.ACCENT
CARD, LINE, WHITE = ig.CARD, ig.LINE, ig.WHITE


def canvas(color):
    return Image.new("RGBA", (W, H), color + (255,))


def display(size, italic=False):
    return ig.fraunces(size, 500 if italic else 530, italic=italic)


def step_num(draw, n, y=104):
    ig.kicker(draw, (M, y), f"{n:02d}")


def dots(draw, index, on_dark):
    total = 6
    r = 5
    gap = 16
    span = total * r * 2 + (total - 1) * gap
    x = (W - span) / 2
    y = 1272
    inactive = (122, 142, 132) if on_dark else (206, 198, 188)
    for i in range(total):
        fill = ACCENT if i == index else inactive
        draw.ellipse((x, y, x + r * 2, y + r * 2), fill=fill)
        x += r * 2 + gap


def cover():
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    mark = ig.scale_w(ig.MARK, 118)
    headline = display(84)
    italic = display(84, italic=True)
    rows = [
        ("From the way", headline),
        ("you coach,", headline),
        ("to the session", headline),
        ("they follow.", italic),
    ]
    block = mark.height + 36 + 28 + 48 + 96 * 4
    y = (H - block) // 2 - 10
    im.alpha_composite(mark, ((W - mark.width) // 2, y))
    y += mark.height + 36
    label = "HOW IT WORKS"
    spacing = 5.4
    width = sum(ig.F_KICKER.getlength(ch) + spacing for ch in label) - spacing
    ig.tracked(draw, ((W - width) / 2, y), label, ig.F_KICKER, ACCENT, spacing)
    y += 64
    ig.centered(draw, W / 2, y, rows, PAPER, 96)
    dots(draw, 0, True)
    return im


def train():
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    step_num(draw, 1)
    ig.lines(
        draw,
        (M, 188),
        [("Train it", display(108)), ("once.", display(108, italic=True))],
        INK,
        114,
    )
    ig.lines(
        draw,
        (M, 470),
        [
            ("On how you coach, and the", ig.F_BODY),
            ("programs you already write.", ig.F_BODY),
        ],
        MUTED,
        42,
    )
    items = [
        ("How you coach", "A short voice is enough."),
        ("Programs you write", "Two or three is enough to start."),
        ("A voice that sounds like you", "The next pass sounds like the studio."),
    ]
    y = 640
    for title, detail in items:
        draw.ellipse((M, y + 10, M + 14, y + 24), fill=ACCENT)
        draw.text((M + 36, y), title, font=ig.sans(32, 560), fill=INK, anchor="lt")
        draw.text((M + 36, y + 42), detail, font=ig.F_SMALL, fill=MUTED, anchor="lt")
        y += 130
    dots(draw, 1, False)
    return im


def draft_card():
    w = W - M * 2
    h = 520
    card = ig.make_card(w, h, 44)
    d = ImageDraw.Draw(card)
    pad = 40
    ig.kicker(d, (pad, 36), "The brief")
    brief = display(40, italic=True)
    d.text((pad, 84), "Two days a week.", font=brief, fill=INK, anchor="lt")
    d.text((pad, 136), "Wants to press again.", font=brief, fill=INK, anchor="lt")
    d.line((pad, 210, w - pad, 210), fill=LINE, width=2)
    ig.kicker(d, (pad, 236), "The draft")
    rows = [
        ("Goblet squat", "3 × 8"),
        ("Push-up", "3 × 10"),
        ("Dead bug", "3 × 1 min"),
    ]
    y = 292
    for name, dose in rows:
        d.text((pad, y), name, font=ig.sans(30, 560), fill=INK, anchor="lt")
        dose_w = ig.F_BODY.getlength(dose)
        d.text((w - pad - dose_w, y), dose, font=ig.F_BODY, fill=MUTED, anchor="lt")
        y += 52
    return card


def draft():
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    step_num(draw, 2)
    ig.lines(
        draw,
        (M, 188),
        [("Tell it what", display(100)), ("they need.", display(100, italic=True))],
        PAPER,
        108,
    )
    ig.lines(
        draw,
        (M, 440),
        [
            ("The program takes shape.", ig.F_BODY),
            ("They only see it after you save.", ig.F_BODY),
        ],
        (214, 206, 196),
        42,
    )
    ig.paste_card(im, draft_card(), (M, 600), 44)
    dots(draw, 2, True)
    return im


def exercise():
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    step_num(draw, 3)
    ig.lines(
        draw,
        (M, 188),
        [("Sets, cues,", display(100)), ("a video.", display(100, italic=True))],
        INK,
        108,
    )
    ig.lines(
        draw,
        (M, 440),
        [
            ("Already on every exercise.", ig.F_BODY),
            ("Pulled from your library.", ig.F_BODY),
        ],
        MUTED,
        42,
    )
    ig.paste_card(im, ig.exercise_card(), (M, 600), 44)
    dots(draw, 3, False)
    return im


def brand():
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    step_num(draw, 4)
    ig.lines(
        draw,
        (M, 188),
        [("Branded", display(108)), ("as yours.", display(108, italic=True))],
        PAPER,
        114,
    )
    draw.text(
        (M, 460),
        "Turn off anything you don't want.",
        font=ig.F_BODY,
        fill=(214, 206, 196),
        anchor="lt",
    )
    ig.paste_card(im, ig.branded_card(0), (M, 560), 44)
    dots(draw, 4, True)
    return im


def phone():
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    step_num(draw, 5)
    ig.lines(
        draw,
        (M, 176),
        [("They open it", display(92)), ("and just train.", display(92, italic=True))],
        PAPER,
        100,
    )
    shot = ig.scale_w(ig.PHONE, 860)
    im.alpha_composite(shot, ((W - shot.width) // 2, 430))
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    slides = [
        ("01-cover.png", cover()),
        ("02-train.png", train()),
        ("03-draft.png", draft()),
        ("04-exercise.png", exercise()),
        ("05-branded.png", brand()),
        ("06-phone.png", phone()),
    ]
    cell_w = 280
    cell_h = round(cell_w * H / W)
    gap = 16
    pad = 24
    board = Image.new("RGB", (pad * 2 + 6 * cell_w + 5 * gap, cell_h + pad * 2), (255, 255, 255))
    for i, (name, im) in enumerate(slides):
        path = OUT / name
        ig.finish(im).save(path, "PNG", optimize=True)
        print(path.name)
        tile = im.convert("RGB").resize((cell_w, cell_h), Image.Resampling.LANCZOS)
        board.paste(tile, (pad + i * (cell_w + gap), pad))
    preview = ROOT / "carousel-preview.png"
    board.save(preview, "PNG", optimize=True)
    print(preview)


if __name__ == "__main__":
    main()
