#!/usr/bin/env python3
"""Convert WinMUGEN SFF v1 sprites to JSON/PNG and rebuild them."""

import argparse
import io
import json
import struct
from pathlib import Path

from PIL import Image


HEADER_SIZE = 512
SUBHEADER_SIZE = 32
SIGNATURE = b"ElecbyteSpr\x00"
DEFAULT_PALETTE = Path("docs/scripts/pallet.act")


def read_sff(path):
    data = path.read_bytes()
    if len(data) < HEADER_SIZE or data[:12] != SIGNATURE:
        raise ValueError("SFF v1 header is not valid")
    records = []
    offset = struct.unpack_from("<I", data, 24)[0]
    visited = set()
    while offset:
        if offset in visited or offset + SUBHEADER_SIZE > len(data):
            raise ValueError("SFF subheader chain is invalid")
        visited.add(offset)
        next_offset, length = struct.unpack_from("<II", data, offset)
        x_axis, y_axis, group, index = struct.unpack_from("<hhHH", data, offset + 8)
        palette_shared = struct.unpack_from("<H", data, offset + 18)[0] != 0
        start = offset + SUBHEADER_SIZE
        end = start + length
        if end > len(data):
            raise ValueError("SFF sprite data is truncated")
        records.append({
            "offset": offset,
            "next": next_offset,
            "x": x_axis,
            "y": y_axis,
            "group": group,
            "index": index,
            "palette_shared": palette_shared,
            "pcx": data[start:end],
        })
        if next_offset == len(data):
            break
        offset = next_offset
    return data[:HEADER_SIZE], records


def read_pcx_palette(data):
    if len(data) < 769 or data[-769] != 12:
        raise ValueError("unshared PCX does not contain a palette")
    palette_data = data[-768:]
    palette = []
    for offset in range(0, len(palette_data), 3):
        palette.append(tuple(palette_data[offset:offset + 3]))
    return palette


def read_act(path):
    data = path.read_bytes()
    if len(data) != 768:
        raise ValueError("ACT palette must contain exactly 768 bytes")
    return [tuple(data[offset:offset + 3]) for offset in range(0, 768, 3)]


def write_png(record, output, palette):
    image = Image.open(io.BytesIO(record["pcx"]))
    image.load()
    indexed = image if image.mode == "P" else image.convert("L")
    pixels = indexed.load()
    rgba = []
    for y in range(indexed.height):
        for x in range(indexed.width):
            index = pixels[x, y]
            color = palette[index]
            alpha = 0 if index == 0 else 255
            rgba.append((color[0], color[1], color[2], alpha))
    output_image = Image.new("RGBA", indexed.size)
    output_image.putdata(rgba)
    output_image.save(output, format="PNG")


def export_sff(sff_path, json_path, image_dir):
    header, records = read_sff(sff_path)
    fallback_palette = read_act(DEFAULT_PALETTE)
    image_dir.mkdir(parents=True, exist_ok=True)
    sprites = []
    previous_palette = None
    for number, record in enumerate(records):
        filename = "{:04d}_{:04d}.png".format(record["group"], record["index"])
        if record["palette_shared"]:
            if previous_palette is None:
                palette = fallback_palette
            else:
                palette = previous_palette
        else:
            palette = read_pcx_palette(record["pcx"])
            previous_palette = palette
        write_png(record, image_dir / filename, palette)
        sprites.append({
            "group": record["group"],
            "index": record["index"],
            "axis": [record["x"], record["y"]],
            "image": filename,
            "palette_shared": record["palette_shared"],
            "palette_hex": bytes(value for color in palette for value in color).hex(),
        })
    document = {
        "format": "winmugen-sff-v1",
        "header_hex": header.hex(),
        "sprites": sprites,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("exported: {} sprites".format(len(records)))


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


def read_png_palette(path):
    with Image.open(path) as image:
        if image.mode != "P":
            return None
        values = list(image.getpalette() or [])
    while len(values) < 768:
        values.append(0)
    return [tuple(values[offset:offset + 3]) for offset in range(0, 768, 3)]


def encode_pcx(path, palette):
    image = Image.open(path).convert("RGBA")
    top_left = image.getpixel((0, 0))
    transparent = top_left[:3]
    use_transparent_rgb = top_left[3] != 0
    pixels = image.load()
    indexes = []
    cache = {}
    for y in range(image.height):
        for x in range(image.width):
            pixel = pixels[x, y]
            rgb = pixel[:3]
            if pixel[3] == 0 or (use_transparent_rgb and pixel[:3] == transparent):
                index = 0
            else:
                index = cache.get(rgb)
                if index is None:
                    index = nearest_index(rgb, palette)
                    cache[rgb] = index
            indexes.append(index)
    indexed = Image.new("P", image.size)
    indexed.putdata(indexes)
    flat_palette = [value for color in palette for value in color]
    indexed.putpalette(flat_palette)
    result = io.BytesIO()
    indexed.save(result, format="PCX")
    return result.getvalue()


def import_sff(json_path, image_root, output):
    document = json.loads(json_path.read_text(encoding="utf-8"))
    if document.get("format") != "winmugen-sff-v1":
        raise ValueError("unsupported sprite JSON format")
    header = bytes.fromhex(document["header_hex"])
    if len(header) != HEADER_SIZE:
        raise ValueError("sprite JSON header is not 512 bytes")
    sprites = document.get("sprites", [])
    if not isinstance(sprites, list):
        raise ValueError("sprites must be a list")
    output_data = bytearray(header)
    shared_palette = read_act(DEFAULT_PALETTE)
    offsets = []
    for sprite in sprites:
        image_path = image_root / Path(sprite["image"])
        if not image_path.is_file():
            image_path = image_root.parent / Path(sprite["image"])
        if not image_path.is_file():
            raise FileNotFoundError(str(image_path))
        shared_group = int(sprite["group"]) < 10000
        shared = shared_group and len(offsets) > 0
        image_palette = read_png_palette(image_path)
        if shared_group:
            palette = shared_palette
        elif image_palette is not None:
            palette = image_palette
        else:
            palette_hex = sprite.get("palette_hex")
            if not palette_hex or len(palette_hex) != 1536:
                raise ValueError("sprite palette_hex must contain 768 bytes")
            palette_data = bytes.fromhex(palette_hex)
            palette = [tuple(palette_data[offset:offset + 3]) for offset in range(0, 768, 3)]
        if image_path.suffix.lower() == ".pcx" and not shared_group:
            pcx = image_path.read_bytes()
            read_pcx_palette(pcx)
        else:
            pcx = encode_pcx(image_path, palette)
        axis = sprite.get("axis", [0, 0])
        offset = len(output_data)
        offsets.append(offset)
        output_data.extend(b"\x00" * SUBHEADER_SIZE)
        output_data.extend(pcx)
        struct.pack_into("<I", output_data, offset + 4, len(pcx))
        struct.pack_into("<hhHH", output_data, offset + 8, int(axis[0]), int(axis[1]), int(sprite["group"]), int(sprite["index"]))
        struct.pack_into("<H", output_data, offset + 18, 1 if shared else 0)
    for number, offset in enumerate(offsets):
        next_offset = offsets[number + 1] if number + 1 < len(offsets) else 0
        struct.pack_into("<I", output_data, offset, next_offset)
    struct.pack_into("<I", output_data, 20, len(offsets))
    struct.pack_into("<I", output_data, 24, offsets[0] if offsets else 0)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(output_data)
    print("imported: {} sprites".format(len(offsets)))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    export_parser = subparsers.add_parser("sff-to-json")
    export_parser.add_argument("--input", dest="sff", type=Path, required=True)
    export_parser.add_argument("--output-json", dest="json", type=Path, required=True)
    export_parser.add_argument("--output-png", dest="image_dir", type=Path, required=True)
    import_parser = subparsers.add_parser("json-to-sff")
    import_parser.add_argument("--input-json", dest="json", type=Path, required=True)
    import_parser.add_argument("--input-png", dest="image_root", type=Path, required=True)
    import_parser.add_argument("--output", dest="sff", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "sff-to-json":
        export_sff(args.sff, args.json, args.image_dir)
    else:
        import_sff(args.json, args.image_root, args.sff)


if __name__ == "__main__":
    main()
