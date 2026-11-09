#!/usr/bin/env python3
"""Install this pet locally with checksum verification and automatic backups."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone

PET_ID = 'doraemon-theatrical'
FILES = ('pet.json', 'spritesheet.webp')


def install(source, codex_home, dry_run=False):
    source, codex_home = Path(source), Path(codex_home).expanduser()
    manifest = json.loads((source / 'pet.json').read_text(encoding='utf-8'))
    if (manifest.get('id'), manifest.get('spriteVersionNumber'), manifest.get('spritesheetPath')) != (PET_ID, 1, 'spritesheet.webp'):
        raise ValueError('Unexpected pet manifest; no files were installed.')
    checks = {}
    for line in (source / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        checks[name.strip()] = digest
    for name in FILES:
        actual = hashlib.sha256((source / name).read_bytes()).hexdigest()
        if checks.get(name) != actual:
            raise ValueError(f'Checksum mismatch: {name}; no files were installed.')
    pets = codex_home / 'pets'
    destination = pets / PET_ID
    if destination.is_symlink() or any((destination / name).is_symlink() for name in FILES):
        raise ValueError('Destination contains a symlink; refusing to replace it.')
    if destination.exists() and not destination.is_dir():
        raise ValueError('Destination exists and is not a directory.')
    if dry_run:
        print(f'Would install {PET_ID} into {destination}')
        return destination
    if all((destination / name).is_file() and (destination / name).read_bytes() == (source / name).read_bytes() for name in FILES):
        print(f'Already installed: {destination}')
        return destination
    existing = [name for name in FILES if (destination / name).is_file()]
    if existing:
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')
        backup = pets / '.backups' / f'{PET_ID}-{stamp}'
        backup.mkdir(parents=True, exist_ok=False)
        for name in existing:
            shutil.copy2(destination / name, backup / name)
        print(f'Previous files backed up to {backup}')
    pets.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.doraemon-stage-', dir=pets) as temp:
        stage = Path(temp)
        for name in FILES:
            shutil.copy2(source / name, stage / name)
        destination.mkdir(exist_ok=True)
        for name in FILES:
            os.replace(stage / name, destination / name)
    print(f'Installed: {destination}')
    print('Open Settings > Pets > Refresh, choose 哆啦A梦 · 剧场版, then enter /pet.')
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-home', type=Path, default=Path(os.environ.get('CODEX_HOME') or Path.home() / '.codex'), help='Codex data directory; defaults to CODEX_HOME or ~/.codex')
    parser.add_argument('--dry-run', action='store_true', help='Verify inputs and print the destination without writing files')
    args = parser.parse_args()
    try:
        install(Path(__file__).resolve().parent, args.codex_home, args.dry_run)
    except (OSError, ValueError) as error:
        parser.exit(1, f'Installation failed: {error}\n')


if __name__ == '__main__':
    main()
