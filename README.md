# TODO

![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A script to search for ``TODO`` notes in a project. It requires no external dependencies. Runs on Python 3.12+.

## Features

- **Clear output** – shows file path and line number for each match.
- **Recursive search** – scans all files in a directory (or a single file) for `TODO:` comments.
- **Case‑insensitive mode** – use `-i` to match `todo:` regardless of case.
- **Exclusion support** – skip default folders (`.git`, `__pycache__`, venvs, etc.) or add your own with `-xd` / `-xf`.
- **No external dependencies** – runs on Python 3.12+ with only the standard library.
- **Performance stats** – prints total TODO count and execution time in milliseconds.

## Screenshot

![Screenshot](https://images2.imgbox.com/44/5c/knjTMbUa_o.png)

## Usage

```bash
python todo.py [path] [options]
```

_If no path is given, the script searches the current directory._

### Options

| Option                         | Description                                        |
|--------------------------------|----------------------------------------------------|
| `path`                         | File or directory to search (default: `.`)         |
| `-i`, `--ignore-case`          | Match `TODO` case‑insensitively                    |
| `-xf`, `--exclude-files`       | Space‑separated list of file names to exclude      |
| `-xd`, `--exclude-dirs`        | Space‑separated list of directory names to exclude |
| `-xe`, `--exclude-extensions`  | Space‑separated list of file extensions to exclude |
| `-xo`, `--exclude-default-off` | Disable built‑in default exclusions                |
| `-h`, `--help`                 | Show help message                                  |

### Example

Simple use:

```bash
python todo.py
```

Exclude folders (build, dist) and files (.env, config.py), ignore case (-i) and disable default ignored folders and files (-xo):

```bash
python todo.py -xd build dist -xf .env config.py -i -xo
```

After installation according to the Installation section, 
you can use simple `todo` instead of `python todo.py`.

## Installation

**Requirements:** Python 3.12+ (no external dependencies).

1. Clone project

```bash
git clone https://github.com/bulatziyatdinov/todo
```

2. Move into folder

```bash
cd todo
```

3. Create `todo` command

- For Linux:

```bash
chmod +x todo.py
```

```bash
sudo mv todo.py /usr/local/bin/todo
```

- For Windows (PowerShell):

```bash
Add-Content -Path $PROFILE -Value ("`nfunction todo { python '" + (Get-Location).Path + "\todo.py' $args }"); . $PROFILE
```

## License

This project is licensed under the [MIT License](LICENSE).

## Other

### Default Exclusions

The script skips the following folders, files, and file extensions by default 
to avoid scanning irrelevant or generated content. You can override these lists using 
the -xo, -xd, -xf, and -xe options (see **Usage** section):

**Excluded folders:** 

- IDE: .idea, .vscode
- Cache: \_\_pycache__, .ruff_cache, .pytest_cache, .mypy_cache
- Venvs: .venv, venv, .env, env
- Other: .git, build, dist, bin, .DS_Store

**Excluded files:** .env, .env.local, .env.test, .gitignore

**Excluded file extensions:** 

- Text: .pdf, .md, .txt, .log, .docx, .doc
- Data Sources: .json, .csv, .xlsx, .xls
- Databases: .db, .sqlite3
- Media: .mp4, .avi, .mov, .mkv, .mp3, .wav, .ogg, .png, .jpeg, .jpg, .svg, .ico, .bmp
- Other: .env, .lock, .zip, .rar, .7z, .tar, .gz, .bz2, .xz, .tgz, .zst, .temp, .tmp 
.pickle, .pkl, .dat, .bin, .exe, .dll, .so