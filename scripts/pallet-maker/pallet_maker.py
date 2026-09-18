#!/usr/bin/env python3
"""Build a WinMUGEN ACT palette from numbered sprite PNG files."""

import argparse
from pathlib import Path

from PIL import Image


def sprite_group(path):
    prefix = path.stem.split("_", 1)[0]
    try:
        return int(prefix)
    except ValueError:
        return None


def collect_sprites(input_root):
    if not input_root.is_dir():
        raise NotADirectoryError(str(input_root))
    sprites = []
    for path in sorted(input_root.rglob("*.png")):
        group = sprite_group(path)
        if group is not None and group < 10000:
            sprites.append(path)
    if not sprites:
        raise ValueError("no numbered sprites below group 10000")
    return sprites


def extract_palette(sprites):
    first = sprites[0]
    with Image.open(first) as image:
        transparent = image.convert("RGBA").getpixel((0, 0))[:3]
    colors = []
    seen = set()
    for path in sprites:
        print("scan: {}".format(path))
        with Image.open(path) as source:
            image = source.convert("RGBA")
            pixels = image.load()
            for y in range(image.height):
                for x in range(image.width):
                    pixel = pixels[x, y]
                    if pixel[3] != 0 and pixel[:3] not in seen:
                        seen.add(pixel[:3])
                        colors.append(pixel[:3])
    ordered = [transparent]
    ordered.extend(colors)
    if len(ordered) > 256:
        raise ValueError("palette contains {} colors; maximum is 256".format(len(ordered)))
    while len(ordered) < 256:
        ordered.append((0, 0, 0))
    return ordered


def write_act(output, palette):
    data = bytes(value for color in palette for value in color)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(data)
    print("wrote: {} ({} colors)".format(output, len(palette)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sprites = collect_sprites(args.input)
    print("input: {} PNG files".format(len(sprites)))
    palette = extract_palette(sprites)
    write_act(args.output, palette)


if __name__ == "__main__":
    main()
