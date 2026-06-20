#!/usr/bin/env python3

import argparse
import os
import sys
import time
from pathlib import Path

TODO_PREFIX = b'TODO:'

DEFAULT_EXCLUDED_FOLDERS = {
    # IDE stuff
    '.idea',
    '.vscode',
    # Cache
    '__pycache__',
    '.ruff_cache',
    # venvs
    '.venv',
    'venv',
    '.env',
    'env',
    # git
    '.git',
    # Other
    'tests',
}

DEFAULT_EXCLUDED_FILES = {
    '.env',
}


class TodoInfo:
    __slots__ = ['filepath', 'line_number', 'line_str']
    def __init__(self, filepath: Path, line_number: int, line_str: bytes):
        self.filepath = filepath
        self.line_number = line_number
        self.line_str = line_str

    def __str__(self):
        return (f"{self.filepath}:{self.line_number} -> "
                f"{self.line_str.strip().decode('utf-8', errors='replace')}")


def error(content: str, crash: bool = False) -> None:
    print(f'[ERROR] {content}')
    if crash:
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for TODO comments in files",
        add_help=True
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help="Path to file or directory (default: current directory)"
    )
    parser.add_argument(
        '-i',
        '--ignore-case',
        action='store_true',
        help="Enable ignoring case"
    )
    parser.add_argument(
        '-xf',
        '--exclude-files',
        nargs='+',
        help="List of file names to exclude from search"
    )
    parser.add_argument(
        '-xd',
        '--exclude-dirs',
        nargs='+',
        help="List of directory names to exclude from search"
    )
    parser.add_argument(
        '-xo',
        '--exclude-default-off',
        action='store_true',
        help="Disable built-in default exclusions (e.g., .git, __pycache__, venv, etc.)"
    )

    return parser.parse_args()


def find_prefix(line: bytes, settings: dict) -> bool:
    if settings['ignore_case']:
        line = line.lower()
    return settings['todo_prefix'] in line


def process_file(filepath: Path, settings: dict) -> list[TodoInfo]:
    todos = []
    try:
        with open(filepath, 'rb') as f:
            file_text = f.readlines()
        for num, line in enumerate(file_text, 1):
            if find_prefix(line, settings):
                todos.append(TodoInfo(filepath, num, line))
    except OSError:
        error(f'Could not read file "{filepath}"')
    return todos


def process_directory(root_path: Path, settings: dict) -> list[TodoInfo]:
    todos = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in settings['excluded_folders']]
        for file in files:
            if file not in settings['excluded_files']:
                filepath = Path(root) / file
                todos.extend(process_file(filepath, settings))
    return todos


def process_settings(args: argparse.Namespace) -> dict:
    if args.exclude_default_off:
        excluded_folders = set()
        excluded_files = set()
    else:
        excluded_folders = DEFAULT_EXCLUDED_FOLDERS
        excluded_files = DEFAULT_EXCLUDED_FILES

    if args.exclude_dirs is not None:
        excluded_folders |= set(args.exclude_dirs)
    if args.exclude_files is not None:
        excluded_files |= set(args.exclude_files)

    return {
        'path': args.path,
        'ignore_case': args.ignore_case,
        'todo_prefix': TODO_PREFIX.lower() if args.ignore_case else TODO_PREFIX,
        'excluded_folders': excluded_folders,
        'excluded_files': excluded_files,
    }


def main():
    start_time = time.perf_counter()

    settings = process_settings(parse_args())

    start_path = Path(settings['path'])
    
    if not start_path.exists():
        error(f'File or directory "{start_path}" does not exist', True)
    
    if start_path.is_file():
        found_todos = process_file(start_path, settings)
    else:
        found_todos = process_directory(start_path, settings)

    for todo in found_todos:
        print(todo)

    total_time = time.perf_counter() - start_time
    print(('-' * 40 + '\n')* (len(found_todos) > 0) +
          f'Total TODO count: {len(found_todos)} | Time: {total_time * 1000:.3f} ms')


if __name__ == '__main__':
    main()
