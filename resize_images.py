#!/usr/bin/env python3
"""Resize and compress source images in image_data/ for web delivery.

Run this BEFORE ./publish_site_data.sh, so the scrambled .bin twins get
regenerated from the smaller files. Back up the current image_data/
originals somewhere before running this — it overwrites the tracked
plain image files in place.

Requires: pip install pillow
Usage:    python3 resize_images.py
"""
import os
from PIL import Image

IMAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_data")
MAX_EDGE = 1200
JPEG_QUALITY = 82

def main():
	for name in sorted(os.listdir(IMAGE_DIR)):
		if name.endswith(".bin") or not name.lower().endswith((".jpg", ".jpeg", ".png")):
			continue
		path = os.path.join(IMAGE_DIR, name)
		before = os.path.getsize(path)
		with Image.open(path) as im:
			is_jpeg = name.lower().endswith((".jpg", ".jpeg"))
			if is_jpeg:
				im = im.convert("RGB")
			im.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
			save_kwargs = {"quality": JPEG_QUALITY, "optimize": True} if is_jpeg else {"optimize": True}
			im.save(path, **save_kwargs)
		after = os.path.getsize(path)
		print(f"{name}: {before / 1024:.0f} KB -> {after / 1024:.0f} KB")

if __name__ == "__main__":
	main()
