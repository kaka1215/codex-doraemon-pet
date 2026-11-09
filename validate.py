#!/usr/bin/env python3
"""Validate the Codex v1 sprite atlas and optionally unpack its 57 frames."""
from pathlib import Path
import argparse
import hashlib
import json
from PIL import Image

ROWS = [('idle', 6), ('running-right', 8), ('running-left', 8), ('waving', 4), ('jumping', 5), ('failed', 8), ('waiting', 6), ('running', 6), ('review', 6)]


def validate(root, extract_to=None):
    root = Path(root)
    pet = json.loads((root / 'pet.json').read_text(encoding='utf-8'))
    if pet.get('id') != 'doraemon-theatrical' or pet.get('spriteVersionNumber') != 1 or pet.get('spritesheetPath') != 'spritesheet.webp':
        raise ValueError('Invalid Codex v1 manifest')
    checks = (root / 'SHA256SUMS').read_text().splitlines()
    if {line.split(maxsplit=1)[1] for line in checks} != {'pet.json', 'spritesheet.webp'}:
        raise ValueError('Checksum file must cover both installable files')
    for line in checks:
        expected, name = line.split(maxsplit=1)
        if name not in {'pet.json', 'spritesheet.webp'}:
            raise ValueError('Unexpected checksum filename')
        if hashlib.sha256((root / name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Checksum mismatch: {name}')
    with Image.open(root / 'spritesheet.webp') as im:
        if im.format != 'WEBP' or im.size != (1536, 1872) or im.mode != 'RGBA':
            raise ValueError('Expected a transparent RGBA WebP atlas at1536x1872')
        atlas = im.copy()
    pixels = atlas.tobytes()
    if any(pixels[i + 3] == 0 and any(pixels[i:i + 3]) for i in range(0, len(pixels), 4)):
        raise ValueError('Hidden RGB residue in fully transparent pixels')
    for row, (state, count) in enumerate(ROWS):
        for col in range(8):
            cell = atlas.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208))
            bbox = cell.getchannel('A').getbbox()
            if col >= count:
                if bbox is not None:
                    raise ValueError(f'Nonempty padding cell: {state}/{col}')
                continue
            if bbox is None or bbox[0] <= 0 or bbox[1] <= 0 or bbox[2] >= 192 or bbox[3] >= 208:
                raise ValueError(f'Empty or clipped frame: {state}/{col}')
            if extract_to:
                folder = Path(extract_to) / state
                folder.mkdir(parents=True, exist_ok=True)
                target = folder / f'{col:02d}.png'
                if target.exists():
                    raise ValueError(f'Will not overwrite existing frame: {target}')
                cell.save(target)
    return {'ok': True, 'format': 'Codex v1', 'size': [1536, 1872], 'cell': [192, 208], 'states': len(ROWS), 'frames': sum(n for _, n in ROWS), 'spritesheet_sha256': hashlib.sha256((root / 'spritesheet.webp').read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', type=Path, help='Extract all57frames into a new folder')
    args = parser.parse_args()
    try:
        print(json.dumps(validate(Path(__file__).resolve().parent, args.extract), ensure_ascii=False, indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f'Validation failed: {error}\n')


if __name__ == '__main__':
    main()
