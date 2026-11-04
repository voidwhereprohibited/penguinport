# Rename plan: `landfall` package -> `penguinport`

Not done yet. This lists everything that would change when `src/landfall` is renamed.
Do it in one branch, in this order, and run the full test suite after each step.

## 1. Package folder

- `git mv src/landfall src/penguinport` (all modules, `data/`, `scan/`, `linux/` move with it).
- `git mv run_landfall.py run_penguinport.py`.

## 2. Imports (`from landfall...` / `import landfall`)

Replace with `penguinport`. Files and number of import lines:

| File | Import lines |
|---|---|
| `run_landfall.py` | 1 |
| `src/landfall/app.py` | 11 |
| `src/landfall/launcher.py` | 6 |
| `src/landfall/linux/apps.py` | 1 |
| `src/landfall/linux/browsers.py` | 1 |
| `src/landfall/linux/importer.py` | 9 |
| `src/landfall/linux/restore.py` | 1 |
| `src/landfall/linux/system_update.py` | 1 |
| `src/landfall/__main__.py` | 1 |
| `src/landfall/pack.py` | 2 |
| `src/landfall/report.py` | 3 |
| `src/landfall/scan/apps.py` | 1 |
| `src/landfall/scan/hardware.py` | 1 |
| `src/landfall/ui.py` | 4 |
| `tests/conftest.py` | 1 |
| `tests/test_app.py` | 3 |
| `tests/test_browsers.py` | 10 |
| `tests/test_importer_logic.py` | 2 |
| `tests/test_linux.py` | 10 |
| `tests/test_pack.py` | 3 |
| `tests/test_phase1.py` | 10 |
| `tests/test_system_update.py` | 1 |
| `tools/make_screenshots.py` | 10 |

`tests/conftest.py` and any `monkeypatch.setattr("landfall....")` strings in tests change too
(they are included in the counts above if they import; search for the quoted string as well).

## 3. Config and build

| File | What changes |
|---|---|
| `pyproject.toml` | `name = "landfall"` -> `"penguinport"`; script `landfall = "landfall.launcher:main"` -> `penguinport = "penguinport.launcher:main"` |
| `.github/workflows/build.yml` | `--add-data "...src/landfall/data:landfall/data"` (Linux and Windows jobs), `run_landfall.py` (both jobs), `import landfall; print(landfall.__version__)`, `LANDFALL_VERSION`, `path: src/landfall/data/linux`, `--icon src/landfall/data/penguinport.ico` |
| `packaging/linux/nfpm.yaml` | `${LANDFALL_VERSION}`, maintainer "Landfall project", description "Landfall Moving Wizard", `vendor: Landfall`, `src: ./src/landfall/data/penguinport.png` |
| `.gitignore` | `src/landfall/data/linux/`, `src/landfall/data/applogos/` |
| `CONTRIBUTING.md` | `src/landfall/data/app_map.json`, `python run_landfall.py` |
| `README.md` | `PYTHONPATH=src .venv/bin/python -m landfall` |
| `tools/build_app_map.py`, `tools/fetch_logos.py`, `tools/make_screenshots.py` | paths `src/landfall/data/...` and imports |

## 4. Runtime names (decide case by case; some are a file format)

| Where | Name | Note |
|---|---|---|
| `pack.py` `DATA_FOLDER` | `.landfall-data` | **Bundle format.** Renaming breaks bundles made by older versions unless the Linux side looks for both. |
| `pack.py`, `linux/restore.py` `MANIFEST` | `landfall/manifest.json`, `landfall/browsers/<key>/`, `"landfall_version"` key | **Bundle format.** Same: read both old and new names, or leave as is. |
| `linux/browsers.py` | `~/.local/share/landfall/` (temporary password CSV) | Safe to rename. |
| `linux/restore.py`, `linux/importer.py` | `.landfall-unpack-*`, `.landfall-browsers-*` temp folders | Safe to rename. |
| `launcher.py` | `LANDFALL_SNAPSHOT`, `LANDFALL_SELFTEST`, `LANDFALL_MODE` env vars; `landfall-wizard` lock file and local server name; `app._landfall_server` | Safe; update `tools/make_screenshots.py` and any CI/test that sets the env vars. |
| `linux/system_update.py` | `LANDFALL STAGE ...` / `LANDFALL DONE` markers | Internal protocol between the script and its parser in the same file; rename both together. |
| `ui.py` | `app.setDesktopFileName("landfall")` | Already wrong: the desktop entry is `penguinport.desktop`, so the window may not get its icon in the dock. Fix to `"penguinport"`. |

## 5. Comments and docstrings

"Landfall" in docstrings/comments of `__init__.py`, `app.py`, `launcher.py`, `linux/__init__.py`,
`linux/browsers.py`, `linux/importer.py`, `linux/restore.py` (also the stale "Landfall Move" /
"Landfall-bundle.7z" examples), `linux/tips.py`, `sysenv.py`, `theme.py`, `run_landfall.py`,
`tools/build_app_map.py`. Replace with "PenguinPort".

## Done when

`git grep -i landfall` only shows the intentional backward-compatible bundle names (if kept),
and the full test suite plus a packaged-app build pass.
