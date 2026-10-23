#!/usr/bin/env python3
"""Feed ad, 1080×1350. Same ground, stickers, and phone as the stories."""

from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("ig_story", ROOT / "story.py")
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

OUT = ROOT / "ads"
W, H = 1080, 1350


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    im = Image.new("RGBA", (W, H), st.ig.FOREST + (255,))

    st.paste(
        im,
        st.sticker(
            ["build your own app."],
            st.ig.sans(52, 720),
            st.INK,
            st.PAPER,
            2.2,
        ),
        (48, 88),
    )
    st.paste(
        im,
        st.sticker(
            [
                "your name. your colours.",
                "turn off anything you don't run.",
                "they train in your studio.",
            ],
            st.ig.sans(36, 640),
            st.WHITE,
            (24, 22, 20, 235),
            -1.6,
        ),
        (56, 250),
    )
    st.paste(
        im,
        st.sticker(
            ["try for free"],
            st.ig.sans(32, 700),
            st.PAPER,
            st.ACCENT,
            -6.2,
        ),
        (48, 860),
    )
    phone = st.shadowed(
        st.app_shot("01-home.png", 470, 600, inner_top=280, radius=48),
        6,
    )
    st.paste(im, phone, (400, 560))

    path = OUT / "build-your-own-app.png"
    im.convert("RGB").save(path, "PNG")
    print(path)


if __name__ == "__main__":
    main()
