#!/usr/bin/env python3
"""Convert PNG files to a shared ACT palette."""

import argparse
from pathlib import Path

from PIL import Image


def read_act(path):
    data = path.read_bytes()
    if len(data) != 768:
        raise ValueError("ACT palette must contain exactly 768 bytes")
    palette = []
    for offset in range(0, len(data), 3):
        palette.append((data[offset], data[offset + 1], data[offset + 2]))
    return palette


def nearest_index(rgb, palette):
    best_index = 1
    best_distance = None
    for index in range(1, len(palette)):
        color = palette[index]
        red = rgb[0] - color[0]
        green = rgb[1] - color[1]
        blue = rgb[2] - color[2]
        distance = red * red + green * green + blue * blue
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_index = index
    return best_index


def convert_png(input_path, output_path, palette, overwrite):
    if output_path.exists() and not overwrite:
        raise FileExistsError(str(output_path))
    with Image.open(input_path) as source:
        image = source.convert("RGBA")
        transparent = image.getpixel((0, 0))[:3]
        cache = {}
        indexes = []
        pixels = image.load()
        for y in range(image.height):
            for x in range(image.width):
                pixel = pixels[x, y]
                rgb = pixel[:3]
                if pixel[3] == 0 or rgb == transparent:
                    index = 0
                else:
                    index = cache.get(rgb)
                    if index is None:
                        index = nearest_index(rgb, palette)
                        cache[rgb] = index
                indexes.append(index)
        indexed = Image.new("P", image.size)
        indexed.putdata(indexes)
        flat_palette = []
        for color in palette:
            flat_palette.extend(color)
        indexed.putpalette(flat_palette)
        indexed.info["transparency"] = 0
        output_path.parent.mkdir(parents=True, exist_ok=True)
        indexed.save(output_path, format="PNG", optimize=False)


def collect_pngs(input_root):
    if not input_root.is_dir():
        raise NotADirectoryError(str(input_root))
    return sorted(path for path in input_root.rglob("*.png") if path.is_file())


def commonize(palette_path, input_roots, output_root, overwrite):
    palette = read_act(palette_path)
    inputs = []
    for input_root in input_roots:
        for path in collect_pngs(input_root):
            inputs.append((input_root, path))
    if not inputs:
        raise ValueError("no PNG files found")
    print("palette: {}".format(palette_path))
    print("input: {} PNG files".format(len(inputs)))
    for input_root, input_path in inputs:
        relative = input_path.relative_to(input_root)
        output_path = output_root / relative
        print("convert: {} -> {}".format(input_path, output_path))
        convert_png(input_path, output_path, palette, overwrite)
    print("complete: {} PNG files -> {}".format(len(inputs), output_root))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--palette", type=Path, required=True)
    parser.add_argument("--input", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    commonize(args.palette, args.input, args.output, args.overwrite)


if __name__ == "__main__":
    main()
