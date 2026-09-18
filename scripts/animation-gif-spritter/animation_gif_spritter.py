#!/usr/bin/env python3
"""Split an animated GIF into composited PNG frames."""

import argparse
from pathlib import Path

from PIL import Image, ImageSequence


def split_gif(input_path, output_dir):
    if not input_path.is_file():
        raise FileNotFoundError(str(input_path))
    output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(input_path) as gif:
        frames = list(ImageSequence.Iterator(gif))
        if not frames:
            raise ValueError("GIF has no frames")
        outputs = []
        for number, frame in enumerate(frames):
            output = output_dir / "{:04d}.png".format(number)
            if output.exists():
                raise FileExistsError(str(output))
            frame.convert("RGBA").save(output, format="PNG")
            outputs.append(output)
    print("split: {} frames -> {}".format(len(outputs), output_dir))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-png", type=Path, required=True)
    args = parser.parse_args()
    split_gif(args.input, args.output_png)


if __name__ == "__main__":
    main()
