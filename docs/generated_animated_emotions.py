#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "pillow>=12.0.0",
# ]
# ///
import os
from PIL import Image

def natural_sort_key(s: str):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def load_pngs(input_dir: str):
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(".png")]
    files.sort(key=natural_sort_key)
    if not files:
        raise FileNotFoundError("No PNG files found in the input directory.")
    paths = [os.path.join(input_dir, f) for f in files]
    images = [Image.open(p).convert("RGBA") for p in paths]
    return images

def make_gif(input_dir: str, output_path: str, fps: float = 12.0, loop: int = 0, optimize: bool = True, scale: float = 1.0):
    frames = load_pngs(input_dir)
    # Optional scaling
    if scale != 1.0:
        scaled = []
        for im in frames:
            w, h = im.size
            new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
            scaled.append(im.resize(new_size, resample=Image.Resampling.LANCZOS))
        frames = scaled

    # Duration per frame in milliseconds
    duration_ms = int(round(1000.0 / fps))

    # GIF requires palette; Pillow will convert while saving
    first, rest = frames[0], frames[1:]
    first.save(
        output_path,
        save_all=True,
        append_images=rest,
        duration=duration_ms,
        loop=loop,
        optimize=optimize,
        disposal=2  # restore to background (helps with transparency artifacts)
    )
    print(f"Saved GIF to {output_path} with {len(frames)} frames at {fps} FPS.")

if __name__ == "__main__":
    # Iterate over folders in "emotions" path and create GIFs
    for emotion in os.listdir("../Code/emotion"):
        emotion_dir = os.path.join("../Code/emotion", emotion)
        if os.path.isdir(emotion_dir):
            output_gif_path = f"./assets/{emotion}.gif"
            make_gif(input_dir=emotion_dir, output_path=output_gif_path, fps=12, loop=0, optimize=True, scale=0.5)
