"""
Generate Little Future PWA icons.

Run from the backend/ directory:
    python scripts/make_icons.py

Outputs into static/img/pwa/.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "static" / "img" / "pwa"
OUT.mkdir(parents=True, exist_ok=True)

PINK = (247, 182, 194)
PURPLE = (201, 167, 255)
INK = (31, 18, 71)
WHITE = (255, 255, 255)


def gradient(size, c1, c2):
    """Create a 135deg linear gradient image."""
    img = Image.new("RGB", (size, size), c1)
    px = img.load()
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            r = int(c1[0] * (1 - t) + c2[0] * t)
            g = int(c1[1] * (1 - t) + c2[1] * t)
            b = int(c1[2] * (1 - t) + c2[2] * t)
            px[x, y] = (r, g, b)
    return img


def rounded_mask(size, radius):
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=radius, fill=255)
    return mask


def make_icon(size, padding_ratio=0.18, rounded=True, bleed=False):
    """Single PWA icon: rounded gradient square with the LF mark and a sparkle."""
    bg = gradient(size, PINK, PURPLE)
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    if rounded and not bleed:
        canvas.paste(bg, (0, 0), rounded_mask(size, int(size * 0.22)))
    else:
        canvas.paste(bg, (0, 0))

    draw = ImageDraw.Draw(canvas)

    # Soft inner glow
    pad = int(size * padding_ratio)
    glow = Image.new("L", (size, size), 0)
    gd = ImageDraw.Draw(glow)
    gd.ellipse((pad, pad, size - pad, size - pad), fill=120)
    glow = glow.filter(ImageFilter.GaussianBlur(size * 0.05))
    canvas.alpha_composite(Image.merge("RGBA", (
        Image.new("L", (size, size), 255),
        Image.new("L", (size, size), 255),
        Image.new("L", (size, size), 255),
        glow,
    )))

    # Try a system font; fall back to default
    font = None
    for candidate in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/seguibl.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ):
        try:
            font = ImageFont.truetype(candidate, int(size * 0.46))
            break
        except OSError:
            continue
    if font is None:
        font = ImageFont.load_default()

    text = "LF"
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        x = (size - tw) / 2 - bbox[0]
        y = (size - th) / 2 - bbox[1] - size * 0.02
    except AttributeError:  # very old Pillow
        tw, th = font.getsize(text)
        x = (size - tw) / 2
        y = (size - th) / 2

    # Drop shadow
    draw.text((x + max(2, size * 0.01), y + max(2, size * 0.01)), text, font=font, fill=(31, 18, 71, 90))
    # Main letters
    draw.text((x, y), text, font=font, fill=WHITE)

    # Tiny sparkle
    sp = int(size * 0.09)
    sx, sy = int(size * 0.78), int(size * 0.20)
    draw.polygon([
        (sx, sy - sp),
        (sx + sp * 0.25, sy - sp * 0.25),
        (sx + sp, sy),
        (sx + sp * 0.25, sy + sp * 0.25),
        (sx, sy + sp),
        (sx - sp * 0.25, sy + sp * 0.25),
        (sx - sp, sy),
        (sx - sp * 0.25, sy - sp * 0.25),
    ], fill=WHITE)

    return canvas


def main():
    sizes = [192, 256, 384, 512]
    for size in sizes:
        out = OUT / f"icon-{size}.png"
        make_icon(size).save(out, "PNG", optimize=True)
        print("wrote", out.relative_to(BASE))

    # Maskable icon: more padding so the safe zone fills 80% of the canvas
    maskable = make_icon(512, padding_ratio=0.30, rounded=False, bleed=True)
    out = OUT / "icon-maskable-512.png"
    maskable.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(BASE))

    # Apple touch icon
    apple = make_icon(180, padding_ratio=0.18, rounded=True)
    out = OUT / "apple-touch-icon.png"
    apple.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(BASE))

    # Favicon
    fav = make_icon(64, padding_ratio=0.18, rounded=True)
    out = BASE / "static" / "img" / "favicon.png"
    fav.save(out, "PNG", optimize=True)
    print("wrote", out.relative_to(BASE))


if __name__ == "__main__":
    main()
