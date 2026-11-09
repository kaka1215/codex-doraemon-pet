# Doraemon · Codex Pet

[中文](README.md)

An unofficial Doraemon desktop companion for Codex, in a flat Japanese 2D animation style: **9 states and 57 frames**.

<p align="center"><img src="preview.gif" width="720" alt="Nine Doraemon pet animation states"></p>

This is an independent fan project, not affiliated with or endorsed by OpenAI or the Doraemon rights holders. Original code and documentation are MIT licensed. Character artwork is excluded; see [asset rights](ASSET_RIGHTS.md).

## Install

Download **Code → Download ZIP** and extract it, or clone:

```sh
git clone https://github.com/kaka1215/codex-doraemon-pet.git
cd codex-doraemon-pet
python3 install.py
```

On Windows, use `py install.py`. The installer uses only the Python standard library. It checks SHA-256 hashes, installs the two pet files into `$CODEX_HOME/pets/doraemon-theatrical/` (default: `~/.codex/pets/doraemon-theatrical/`), and backs up changed existing files under `pets/.backups/`. Reinstalling identical files does nothing.

```sh
python3 install.py --dry-run
python3 install.py --codex-home "/path/to/codex-data"
```

You can also copy `pet.json` and `spritesheet.webp` into that directory manually.

Open **Settings → Pets → Refresh**, choose **哆啦A梦 · 剧场版**, then enter **`/pet`** or choose **Show pet**. Resize it through **Customize → Pet size**. See the [official Pets guide](https://learn.chatgpt.com/docs/pets). This package targets local desktop pets and does not automatically sync to the web.

## Run cycle

<p align="center"><img src="run-preview.gif" width="720" alt="Left and right run cycles beside the idle pose"></p>

The run has forward reach, push-off, recovery and flight. It is a simplified cartoon cycle; some opposite half-cycle arm positions repeat. Previews use the desktop cadence of seven 120 ms phases plus one 220 ms phase. The longer phase is grounded contact.

## Format and development

- Codex sprite v1, transparent RGBA WebP, **1536 × 1872**.
- **8 columns × 9 rows**, **192 × 208** per cell.
- Row counts: `idle`6, `running-right`8, `running-left`8, `waving`4, `jumping`5, `failed`8, `waiting`6, `running`6, `review`6.
- `running` is task processing; directional rows are locomotion.
- 57 populated cells and 15 transparent padding cells.

```sh
python3 -m pip install -r requirements.txt
python3 validate.py
python3 -m unittest -v test_install.py
python3 validate.py --extract frames
```

The validator checks geometry, alpha, occupied/unused cells, clipping and transparent RGB residue. Extraction refuses to overwrite existing frame files. Installer tests use isolated temporary directories. Update `SHA256SUMS` after modifying the installable files.

See [DESIGN.md](DESIGN.md) for the workflow and a reusable prompt. Artwork was made with built-in ImageGen and the official [hatch-pet skill](https://github.com/openai/skills/tree/main/skills/.curated/hatch-pet). Upstream skill implementation is not vendored here.

## License

Original code and documentation: [MIT](LICENSE). Doraemon character names and designs belong to their respective rights holders. PNG, GIF and WebP artwork is excluded from that grant. This repository grants no commercial character rights or right to sublicense the character. See [ASSET_RIGHTS.md](ASSET_RIGHTS.md).
