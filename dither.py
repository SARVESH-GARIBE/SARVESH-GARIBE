#!/usr/bin/env python3
"""
Turn any photo into a 1-bit dithered pixel image (the retro "Mac" look).

usage:
  python3 dither.py input.jpg output.png [width] [pixel_size]

  width       how many "pixels" wide the art is   (default 160)
  pixel_size  how big each pixel is drawn          (default 3)

examples:
  python3 dither.py me.jpg avatar.png 120 3       # portrait for About Me
  python3 dither.py banner.jpg banner.png 240 3   # wide banner
"""
import sys
from PIL import Image, ImageOps, ImageEnhance

src, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 160
px = int(sys.argv[4]) if len(sys.argv) > 4 else 3

img = Image.open(src).convert("L")
img = ImageOps.autocontrast(img, cutoff=2)
img = ImageEnhance.Contrast(img).enhance(1.4)

h = int(img.height * width / img.width)
img = img.resize((width, h), Image.LANCZOS)

# Floyd–Steinberg dithering to pure black/white
bw = img.convert("1")

# scale up with hard edges so pixels stay crisp
bw = bw.resize((width * px, h * px), Image.NEAREST).convert("L")

# white pixels on transparent background, so it sits on GitHub's dark theme
rgba = Image.new("RGBA", bw.size, (0, 0, 0, 0))
white = Image.new("RGBA", bw.size, (230, 237, 243, 255))
rgba.paste(white, mask=bw)
rgba.save(out)
print(f"saved {out}  ({rgba.width}x{rgba.height})")
