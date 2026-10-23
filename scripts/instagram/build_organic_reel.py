#!/usr/bin/env python3
"""Build an Organic Instagram Reel video for Studio Health using generated footage and animated overlays."""

import math
import shutil
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
FOOTAGE = ROOT / "posts" / "reel_footage.mp4"
OUT_REEL = ROOT / "posts" / "organic_reel_01.mp4"

NEW_YORK = Path("/System/Library/Fonts/NewYork.ttf")
NEW_YORK_ITALIC = Path("/System/Library/Fonts/NewYorkItalic.ttf")
SF = Path("/System/Library/Fonts/SFNS.ttf")

W, H = 1080, 1920
FPS = 30

FOREST = (61, 83, 72)
PAPER = (243, 238, 230)
INK = (27, 24, 20)
ACCENT = (196, 92, 38)
YELLOW = (255, 212, 59)
WHITE = (255, 255, 255)

def sans(size: int, weight: int = 600):
    font = ImageFont.truetype(str(SF), size)
    font.set_variation_by_axes([100, max(17, min(96, size)), 400, weight])
    return font

def serif(size: int, italic: bool = False):
    font_path = NEW_YORK_ITALIC if italic else NEW_YORK
    return ImageFont.truetype(str(font_path), size)

F_HOOK_TITLE = serif(48)
F_HOOK_SUB = sans(34, 600)
F_SUBTITLE = sans(44, 700)
F_BADGE = sans(24, 700)

def extract_frames():
    tmp_in = Path("/tmp/sh_reel_raw")
    if tmp_in.exists():
        shutil.rmtree(tmp_in)
    tmp_in.mkdir(parents=True)
    subprocess.run([
        "ffmpeg", "-y", "-i", str(FOOTAGE),
        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
        "-r", str(FPS),
        str(tmp_in / "f_%04d.png")
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted(list(tmp_in.glob("f_*.png")))

def draw_hook_card(draw_base, t):
    """0s to 3.2s: Viral Hook card at top-middle."""
    if t > 3.5:
        return
    
    alpha = 1.0
    if t > 3.0:
        alpha = (3.5 - t) / 0.5
    
    card_w = 940
    card_h = 320
    cx, cy = W // 2, 420
    x0, y0 = cx - card_w // 2, cy - card_h // 2
    
    card = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    
    # Shadow + Card background
    d.rounded_rectangle((0, 0, card_w, card_h), radius=36, fill=(243, 238, 230, int(245 * alpha)))
    d.rounded_rectangle((0, 0, card_w, card_h), radius=36, outline=(196, 92, 38, int(255 * alpha)), width=4)
    
    # Header tag
    d.rounded_rectangle((36, 32, 280, 72), radius=12, fill=(196, 92, 38, int(255 * alpha)))
    d.text((52, 42), "STUDIO OWNER TIP", font=F_BADGE, fill=(255, 255, 255, int(255 * alpha)))
    
    # Text
    d.text((36, 92), "I stopped spending 6 hours", font=serif(44), fill=(27, 24, 20, int(255 * alpha)))
    d.text((36, 146), "every Sunday writing workouts.", font=serif(44, italic=True), fill=(27, 24, 20, int(255 * alpha)))
    d.text((36, 218), "Here is how to do it in 60 seconds 👇", font=sans(32, 600), fill=(111, 103, 92, int(255 * alpha)))
    
    # Composite card onto draw_base
    draw_base.paste(card, (x0, y0), card)

def draw_subtitles(draw_base, t):
    """Dynamic word/phrase highlighted subtitles at bottom third."""
    subtitles = [
        (0.0, 2.4, [("Stop wasting", WHITE), ("Sunday nights", YELLOW), ("on workout programs.", WHITE)]),
        (2.4, 5.2, [("Train your AI once", YELLOW), ("on your coaching style & videos.", WHITE)]),
        (5.2, 8.0, [("Draft custom 4-week plans", WHITE), ("in 60s on Studio Health.", YELLOW)]),
    ]
    
    current_phrases = None
    for start, end, phrases in subtitles:
        if start <= t < end:
            current_phrases = phrases
            break
            
    if not current_phrases:
        return
        
    bar_y = 1450
    
    total_text = " ".join([p[0] for p in current_phrases])
    bbox = F_SUBTITLE.getbbox(total_text)
    tw = bbox[2] - bbox[0]
    
    padding_x = 36
    padding_y = 20
    rect_w = min(W - 80, tw + padding_x * 2)
    rect_h = 130
    rect_x = (W - rect_w) // 2
    
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    d.rounded_rectangle((rect_x, bar_y, rect_x + rect_w, bar_y + rect_h), radius=28, fill=(18, 22, 20, 210))
    
    curr_x = rect_x + (rect_w - tw) // 2
    text_y = bar_y + 36
    
    for text, color in current_phrases:
        d.text((curr_x, text_y), text + " ", font=F_SUBTITLE, fill=color + (255,))
        w_part = F_SUBTITLE.getlength(text + " ")
        curr_x += w_part
        
    draw_base.paste(overlay, (0, 0), overlay)

def draw_branding_watermark(draw_base):
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    
    d.text((60, 80), "studiohealth.ai", font=sans(30, 700), fill=(255, 255, 255, 220))
    draw_base.paste(overlay, (0, 0), overlay)

def process_reel():
    print("Extracting raw footage frames...")
    frame_paths = extract_frames()
    num_frames = len(frame_paths)
    print(f"Extracted {num_frames} frames.")
    
    tmp_out = Path("/tmp/sh_reel_processed")
    if tmp_out.exists():
        shutil.rmtree(tmp_out)
    tmp_out.mkdir(parents=True)
    
    for idx, fpath in enumerate(frame_paths):
        t = idx / FPS
        im = Image.open(fpath).convert("RGBA")
        
        draw_hook_card(im, t)
        draw_subtitles(im, t)
        draw_branding_watermark(im)
        
        im.convert("RGB").save(tmp_out / f"f_{idx:04d}.png")
        
    print("Encoding final Organic Reel video with FFmpeg...")
    subprocess.run([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(tmp_out / "f_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        "-movflags", "+faststart",
        str(OUT_REEL)
    ], check=True)
    
    print(f"Organic Reel generated successfully: {OUT_REEL} ({OUT_REEL.stat().st_size // 1024} KB)")

if __name__ == "__main__":
    process_reel()
