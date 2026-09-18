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
            "pcx": data[start:end],
        })
        if next_offset == len(data):
            break
        offset = next_offset
    return data[:HEADER_SIZE], records


def write_png(record, output):
    image = Image.open(io.BytesIO(record["pcx"]))
    image.load()
    image.save(output, format="PNG")


def export_sff(sff_path, json_path, image_dir):
    header, records = read_sff(sff_path)
    image_dir.mkdir(parents=True, exist_ok=True)
    sprites = []
    for number, record in enumerate(records):
        filename = "{:04d}_{:04d}.png".format(record["group"], record["index"])
        write_png(record, image_dir / filename)
        sprites.append({
            "group": record["group"],
            "index": record["index"],
            "axis": [record["x"], record["y"]],
            "image": filename,
        })
    document = {
        "format": "winmugen-sff-v1",
        "header_hex": header.hex(),
        "sprites": sprites,
    }
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("exported: {} sprites".format(len(records)))


def encode_pcx(path):
    image = Image.open(path).convert("RGBA")
    alpha = image.getchannel("A")
    rgb = Image.new("RGB", image.size, (0, 0, 0))
    rgb.paste(image, mask=alpha)
    indexed = rgb.quantize(colors=255, method=Image.Quantize.MEDIANCUT)
    pixels = indexed.load()
    alpha_pixels = alpha.load()
    for y in range(image.height):
        for x in range(image.width):
            if alpha_pixels[x, y] == 0:
                pixels[x, y] = 0
    palette = list(indexed.getpalette() or [])
    while len(palette) < 768:
        palette.append(0)
    palette[0:3] = [0, 0, 0]
    indexed.putpalette(palette)
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
    offsets = []
    for sprite in sprites:
        image_path = image_root / Path(sprite["image"]).name
        if not image_path.is_file():
            raise FileNotFoundError(str(image_path))
        pcx = encode_pcx(image_path)
        axis = sprite.get("axis", [0, 0])
        offset = len(output_data)
        offsets.append(offset)
        output_data.extend(b"\x00" * SUBHEADER_SIZE)
        output_data.extend(pcx)
        struct.pack_into("<I", output_data, offset + 4, len(pcx))
        struct.pack_into("<hhHH", output_data, offset + 8, int(axis[0]), int(axis[1]), int(sprite["group"]), int(sprite["index"]))
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
