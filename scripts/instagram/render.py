#!/usr/bin/env python3
"""Studio Health Instagram grid: 1080 stills and short silent loops."""

from __future__ import annotations

import math
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "posts"
ICON = Path(
    "/Users/kalehanby/Documents/GitHub/studio-health-docs/app-store/assets/icon-1024.png"
)
PHONE_SRC = Path(
    "/Users/kalehanby/Documents/GitHub/studio-health-docs/app-store/assets/screenshots/iphone-6.9/02-today.png"
)
FRAUNCES = Path("/tmp/sh-fonts/fraunces.ttf")
FRAUNCES_ITALIC = Path("/tmp/sh-fonts/fraunces-italic.ttf")
SF = Path("/System/Library/Fonts/SFNS.ttf")

S = 1080
MARGIN = 88
FOREST = (61, 83, 72)
PAPER = (243, 238, 230)
INK = (27, 24, 20)
MUTED = (111, 103, 92)
ACCENT = (196, 92, 38)
CARD = (255, 251, 245)
LINE = (228, 219, 208)
WHITE = (255, 251, 245)
PHONE_BG = (47, 66, 56)

FPS = 30
SECONDS = 4


def fraunces(size: int, weight: int = 520, italic: bool = False, soft: int = 28):
    font = ImageFont.truetype(str(FRAUNCES_ITALIC if italic else FRAUNCES), size)
    font.set_variation_by_axes([144, weight, soft, 0])
    return font


def sans(size: int, weight: int = 460):
    font = ImageFont.truetype(str(SF), size)
    opsz = max(17, min(96, size))
    font.set_variation_by_axes([100, opsz, 400, weight])
    return font


F_KICKER = sans(22, 560)
F_BODY = sans(30, 450)
F_BODY_MED = sans(32, 560)
F_SMALL = sans(26, 450)
F_TINY = sans(22, 500)


def canvas(color) -> Image.Image:
    return Image.new("RGBA", (S, S), color + (255,))


def tracked(draw, xy, text, font, fill, tracking):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="lt")
        x += font.getlength(ch) + tracking
    return x


def kicker(draw, xy, text, color=ACCENT):
    tracked(draw, xy, text.upper(), F_KICKER, color, 5.2)


def lines(draw, xy, rows, fill, leading):
    """rows: list of (text, font). Returns y after the block."""
    x, y = xy
    for text, font in rows:
        draw.text((x, y), text, font=font, fill=fill, anchor="lt")
        y += leading
    return y


def centered(draw, cx, y, rows, fill, leading):
    for text, font in rows:
        w = font.getlength(text)
        draw.text((cx - w / 2, y), text, font=font, fill=fill, anchor="lt")
        y += leading
    return y


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def make_card(w, h, radius=40, fill=CARD):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=fill + (255,))
    return im


def paste_card(base, card, xy, radius=40):
    x, y = xy
    blur = 26
    pad = blur * 2
    sh = Image.new("RGBA", (card.width + pad * 2, card.height + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle(
        (pad, pad + 8, pad + card.width, pad + 8 + card.height),
        radius=radius,
        fill=(27, 24, 20, 36),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(sh, (x - pad, y - pad))
    base.alpha_composite(card, (x, y))


def chroma(im: Image.Image, bg, cutoff=10, gain=14) -> Image.Image:
    plate = Image.new("RGB", im.size, bg)
    diff = ImageChops.difference(im.convert("RGB"), plate).convert("L")
    alpha = diff.point(lambda p: 0 if p < cutoff else min(255, int((p - cutoff) * gain)))
    rgba = im.convert("RGBA")
    rgba.putalpha(alpha)
    return rgba


def load_mark():
    im = Image.open(ICON).convert("RGB")
    rgba = chroma(im, FOREST, cutoff=12, gain=16)
    alpha = rgba.getchannel("A")
    bbox = alpha.point(lambda p: 255 if p > 24 else 0).getbbox()
    sprite = rgba.crop(bbox)
    # Split on the empty band between the circle and the bowl.
    px = sprite.getchannel("A").load()
    gap_start = None
    gap_end = None
    for y in range(sprite.height):
        empty = all(px[x, y] < 16 for x in range(0, sprite.width, 2))
        if empty and gap_start is None and y > 40:
            gap_start = y
        elif gap_start is not None and not empty:
            gap_end = y
            break
    mid = (gap_start + gap_end) // 2
    circle = sprite.crop((0, 0, sprite.width, mid))
    bowl = sprite.crop((0, mid, sprite.width, sprite.height))
    return sprite, circle, bowl, mid


def load_phone() -> Image.Image:
    im = Image.open(PHONE_SRC).convert("RGB")
    # Drop the App Store headline. The phone mock starts below it.
    sub = im.crop((0, 470, im.width, im.height))
    rgba = chroma(sub, PHONE_BG, cutoff=8, gain=12)
    bbox = rgba.getchannel("A").point(lambda p: 255 if p > 18 else 0).getbbox()
    return rgba.crop(bbox)


MARK, CIRCLE, BOWL, MARK_SPLIT = load_mark()
PHONE = load_phone()


def scale_w(im: Image.Image, width: int) -> Image.Image:
    height = max(1, round(im.height * width / im.width))
    return im.resize((width, height), Image.Resampling.LANCZOS)


def check_circle(draw, cx, cy, r, on: bool):
    if on:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ACCENT)
        font = sans(int(r * 1.35), 650)
        draw.text((cx, cy - r * 0.06), "✓", font=font, fill=WHITE, anchor="mm")
    else:
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=ACCENT, width=max(3, r // 7))


def ring(draw, box, progress, width=14):
    track = (232, 214, 204)
    # A full arc leaves a seam, so a finished ring is an outline.
    if progress >= 0.995:
        draw.ellipse(box, outline=ACCENT, width=width)
        return
    draw.arc(box, 0, 360, fill=track, width=width)
    if progress > 0.01:
        draw.arc(box, -90, -90 + 360 * progress, fill=ACCENT, width=width)


def toggle(draw, x, y, on: float):
    """on is 0..1, knob slides left to right."""
    w, h = 78, 46
    bg = tuple(round((1 - on) * c0 + on * c1) for c0, c1 in zip((196, 188, 176), INK))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=h // 2, fill=bg)
    knob = 17
    left = x + knob + 6
    right = x + w - knob - 6
    kx = left + (right - left) * on
    cy = y + h / 2
    draw.ellipse((kx - knob, cy - knob, kx + knob, cy + knob), fill=CARD)


def finish(im: Image.Image) -> Image.Image:
    return im.convert("RGB")


def save(im: Image.Image, name: str):
    path = OUT / name
    finish(im).save(path, "PNG", optimize=True)
    print(path.name)


# --- posts -----------------------------------------------------------------

H1 = fraunces(112, 530)
H1I = fraunces(112, 500, italic=True)
H2 = fraunces(96, 530)
H2I = fraunces(96, 500, italic=True)
H3 = fraunces(84, 530)
NUM = fraunces(40, 560)


def post_mark(circle_dy=0, bowl_dy=0) -> Image.Image:
    im = canvas(FOREST)
    width = 548
    circle = scale_w(CIRCLE, width)
    bowl = scale_w(BOWL, width)
    x = (S - width) // 2
    top = (S - (circle.height + bowl.height)) // 2 - 36
    im.alpha_composite(circle, (x, top + circle_dy))
    im.alpha_composite(bowl, (x, top + circle.height + bowl_dy))
    draw = ImageDraw.Draw(im)
    label = "STUDIO HEALTH"
    # Center the tracked line.
    spacing = 6.4
    width_label = sum(F_KICKER.getlength(ch) + spacing for ch in label) - spacing
    tracked(draw, ((S - width_label) / 2, 948), label, F_KICKER, PAPER, spacing)
    return im


def post_keep() -> Image.Image:
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 96), "For coaches")
    rows = [
        ("Keep every", H1),
        ("client", H1),
        ("training.", H1I),
    ]
    lines(draw, (MARGIN, 188), rows, INK, 118)
    draw.text((MARGIN, 900), "In your style. At your studio.", font=F_BODY, fill=MUTED, anchor="lt")
    return im


def phone_scaled(width=860) -> Image.Image:
    return scale_w(PHONE, width)


def post_phone(dy=0, phone=None) -> Image.Image:
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 78), "On their phone")
    rows = [
        ("They open it", H3),
        ("and just train.", fraunces(84, 500, italic=True)),
    ]
    lines(draw, (MARGIN, 132), rows, PAPER, 90)
    if phone is None:
        phone = phone_scaled(900)
    x = (S - phone.width) // 2
    im.alpha_composite(phone, (x, 360 + dy))
    return im


def post_train() -> Image.Image:
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 96), "Your studio AI")
    rows = [("Train it", H1), ("once.", H1I)]
    y = lines(draw, (MARGIN, 176), rows, INK, 116)
    items = [
        ("01", "How you coach"),
        ("02", "Programs you already write"),
        ("03", "Drafts that sound like you"),
    ]
    y = 560
    for num, label in items:
        draw.text((MARGIN, y), num, font=NUM, fill=ACCENT, anchor="lt")
        draw.text((MARGIN + 92, y + 6), label, font=F_BODY_MED, fill=INK, anchor="lt")
        y += 92
    return im


def post_studio() -> Image.Image:
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    rows = [
        ("Your studio.", H1),
        ("Their pocket.", H1I),
    ]
    block_h = 118 * 2
    y = (S - block_h) // 2 - 24
    centered(draw, S / 2, y, rows, PAPER, 118)
    r = 16
    cx, cy = S // 2, y + block_h + 56
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=ACCENT)
    return im


def exercise_card(checks=(True, False, False)) -> Image.Image:
    w = S - MARGIN * 2
    # Built as a content card for post 06, not the checklist.
    h = 470
    card = make_card(w, h, 44)
    d = ImageDraw.Draw(card)
    pad = 40
    check_circle(d, pad + 26, 78, 26, True)
    d.text((pad + 76, 48), "Dumbbell goblet squat", font=F_BODY_MED, fill=INK, anchor="lt")
    d.text((pad + 76, 92), "3 sets  ·  10 reps  ·  Moderate", font=F_SMALL, fill=MUTED, anchor="lt")
    d.line((pad, 156, w - pad, 156), fill=LINE, width=2)
    kicker(d, (pad, 184), "Cue")
    cue = fraunces(40, 480, italic=True)
    d.text((pad, 230), "Chest tall. Drive through", font=cue, fill=INK, anchor="lt")
    d.text((pad, 282), "the heels.", font=cue, fill=INK, anchor="lt")
    # Video chip
    chip_y = 360
    d.rounded_rectangle((pad, chip_y, w - pad, chip_y + 72), radius=20, fill=FOREST)
    d.ellipse((pad + 16, chip_y + 16, pad + 56, chip_y + 56), fill=ACCENT)
    d.polygon(
        [(pad + 32, chip_y + 28), (pad + 32, chip_y + 44), (pad + 46, chip_y + 36)],
        fill=WHITE,
    )
    d.text((pad + 72, chip_y + 20), "How-to video", font=sans(28, 560), fill=PAPER, anchor="lt")
    return card


def post_sets() -> Image.Image:
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 88), "On every exercise")
    rows = [
        ("Sets, cues,", H2),
        ("a video.", H2I),
    ]
    lines(draw, (MARGIN, 156), rows, INK, 102)
    card = exercise_card()
    paste_card(im, card, (MARGIN, 430), 44)
    return im


def today_card(done: float) -> Image.Image:
    """done is 1..3, fractional while a check is drawing on."""
    w = S - MARGIN * 2
    h = 560
    card = make_card(w, h, 44)
    d = ImageDraw.Draw(card)
    pad = 40
    ring_box = (pad, 40, pad + 92, 132)
    ring(d, ring_box, done / 3, width=12)
    d.text((pad + 116, 48), "Today's program", font=F_BODY_MED, fill=INK, anchor="lt")
    shown = sum(1 for i in range(3) if max(0.0, min(1.0, done - i)) > 0.82)
    count = f"{shown} of 3 done"
    d.text((pad + 116, 92), count, font=F_SMALL, fill=MUTED, anchor="lt")
    exercises = [
        ("Goblet squat", "3 × 8  ·  16kg"),
        ("Push-up", "3 × 10 reps"),
        ("Dead bug", "3 × 1 min"),
    ]
    y = 176
    for i, (name, detail) in enumerate(exercises):
        local = max(0.0, min(1.0, done - i))
        on = local > 0.82
        check_circle(d, pad + 28, y + 28, 26, on)
        d.text((pad + 78, y + 4), name, font=F_BODY_MED, fill=INK, anchor="lt")
        d.text((pad + 78, y + 44), detail, font=F_SMALL, fill=MUTED, anchor="lt")
        y += 118
    return card


def post_today(done: float = 1) -> Image.Image:
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 88), "Today's program")
    draw.text((MARGIN, 150), "Today.", font=fraunces(168, 540), fill=PAPER, anchor="lt")
    card = today_card(done)
    paste_card(im, card, (MARGIN, 400), 44)
    return im


TOGGLES = [
    ("Program", 1.0),
    ("Health", 1.0),
    ("Videos", 1.0),
    ("Diet", 0.0),
    ("Booking", 1.0),
]


def branded_card(diet: float = 0.0) -> Image.Image:
    w = S - MARGIN * 2
    row_h = 96
    h = 36 + row_h * len(TOGGLES) + 12
    card = make_card(w, h, 44)
    d = ImageDraw.Draw(card)
    for i, (label, on) in enumerate(TOGGLES):
        value = diet if label == "Diet" else on
        y = 28 + i * row_h
        d.text((40, y + 22), label, font=sans(34, 520), fill=INK, anchor="lt")
        toggle(d, w - 40 - 78, y + 16, value)
        if i < len(TOGGLES) - 1:
            d.line((40, y + row_h - 8, w - 40, y + row_h - 8), fill=LINE, width=2)
    return card


def post_branded(diet: float = 0.0) -> Image.Image:
    im = canvas(PAPER)
    draw = ImageDraw.Draw(im)
    kicker(draw, (MARGIN, 88), "The client app")
    rows = [("Branded", H1), ("as yours.", H1I)]
    lines(draw, (MARGIN, 156), rows, INK, 116)
    draw.text(
        (MARGIN, 400),
        "Turn off anything you don't want.",
        font=F_BODY,
        fill=MUTED,
        anchor="lt",
    )
    card = branded_card(diet)
    paste_card(im, card, (MARGIN, 470), 44)
    return im


def post_built() -> Image.Image:
    im = canvas(FOREST)
    draw = ImageDraw.Draw(im)
    # Small mark, top left, as a bookend to the big mark.
    mark = scale_w(MARK, 92)
    im.alpha_composite(mark, (MARGIN, 88))
    rows = [
        ("Everything", H1),
        ("is built in.", H1I),
    ]
    lines(draw, (MARGIN, 300), rows, PAPER, 118)
    draw.text((MARGIN, 948), "studiohealth.ai", font=sans(28, 520), fill=PAPER, anchor="lt")
    return im


def render_stills():
    OUT.mkdir(parents=True, exist_ok=True)
    save(post_mark(), "01-mark.png")
    save(post_keep(), "02-keep-training.png")
    save(post_phone(), "03-on-their-phone.png")
    save(post_train(), "04-train-it-once.png")
    save(post_studio(), "05-your-studio.png")
    save(post_sets(), "06-sets-cues.png")
    save(post_today(1), "07-today.png")
    save(post_branded(0), "08-branded.png")
    save(post_built(), "09-built-in.png")
    sheet()


def sheet():
    names = [
        "01-mark.png",
        "02-keep-training.png",
        "03-on-their-phone.png",
        "04-train-it-once.png",
        "05-your-studio.png",
        "06-sets-cues.png",
        "07-today.png",
        "08-branded.png",
        "09-built-in.png",
    ]
    cell = 360
    gap = 6
    pad = 18
    w = pad * 2 + cell * 3 + gap * 2
    h = w
    board = Image.new("RGB", (w, h), (255, 255, 255))
    for i, name in enumerate(names):
        tile = Image.open(OUT / name).resize((cell, cell), Image.Resampling.LANCZOS)
        col, row = i % 3, i // 3
        x = pad + col * (cell + gap)
        y = pad + row * (cell + gap)
        board.paste(tile, (x, y))
    path = ROOT / "grid-preview.png"
    board.save(path, "PNG", optimize=True)
    print(path)


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def write_video(name: str, frames: list[Image.Image]):
    tmp = Path(f"/tmp/sh-ig-{name}")
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()
    for i, frame in enumerate(frames):
        frame.convert("RGB").save(tmp / f"f_{i:04d}.png")
    out = OUT / f"{name}.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(FPS),
            "-i",
            str(tmp / "f_%04d.png"),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            "-crf",
            "17",
            "-preset",
            "medium",
            "-movflags",
            "+faststart",
            str(out),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(tmp)
    print(out.name, out.stat().st_size // 1024, "KB")


def video_mark():
    n = FPS * SECONDS
    frames = []
    for i in range(n):
        t = i / n
        circle_dy = round(math.sin(t * math.tau) * 10)
        bowl_dy = round(math.sin(t * math.tau + 0.9) * 4)
        frames.append(finish(post_mark(circle_dy, bowl_dy)))
    write_video("01-mark", frames)


def video_phone():
    n = FPS * SECONDS
    phone = phone_scaled(900)
    frames = []
    for i in range(n):
        t = i / n
        dy = round(math.sin(t * math.tau) * 16)
        frames.append(finish(post_phone(dy, phone)))
    write_video("03-on-their-phone", frames)


def video_today():
    n = FPS * SECONDS
    frames = []
    for i in range(n):
        t = i / n
        # Hold at 1, step to 2, step to 3, hold, settle back at 1.
        if t < 0.16:
            done = 1
        elif t < 0.30:
            done = 1 + smooth((t - 0.16) / 0.14)
        elif t < 0.42:
            done = 2
        elif t < 0.56:
            done = 2 + smooth((t - 0.42) / 0.14)
        elif t < 0.78:
            done = 3
        else:
            done = 3 + (1 - 3) * smooth((t - 0.78) / 0.22)
        frames.append(finish(post_today(done)))
    write_video("07-today", frames)


def video_branded():
    n = FPS * SECONDS
    frames = []
    for i in range(n):
        t = i / n
        if t < 0.18:
            diet = 0
        elif t < 0.34:
            diet = smooth((t - 0.18) / 0.16)
        elif t < 0.62:
            diet = 1
        elif t < 0.78:
            diet = 1 - smooth((t - 0.62) / 0.16)
        else:
            diet = 0
        frames.append(finish(post_branded(diet)))
    write_video("08-branded", frames)


def main():
    render_stills()
    video_mark()
    video_phone()
    video_today()
    video_branded()


if __name__ == "__main__":
    main()
