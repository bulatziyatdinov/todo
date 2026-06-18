#!/usr/bin/env python3

import argparse
import os
import sys
import time
from pathlib import Path

TODO_PREFIX = b'TODO:'

EXCLUDED_FOLDERNAMES_LIST = {
    '.venv',
    'venv',
    '.env',
    'env',
    '.git',
    'tests',
}

EXCLUDED_FILENAMES_LIST = {
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for TODO comments in files.",
        add_help=True
    )
    parser.add_argument('startpath', nargs='?', default='.',
                        help="Path to file or directory (default: current directory)")
    return parser.parse_args()


def process_file(filepath: Path) -> list[TodoInfo]:
    todos = []
    try:
        with open(filepath, 'rb') as f:
            file_text = f.readlines()
        for num, line in enumerate(file_text, 1):
            if TODO_PREFIX in line:
                todos.append(TodoInfo(filepath, num, line))
    except OSError:
        pass
    return todos


def process_directory(root_path: Path) -> list[TodoInfo]:
    todos = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERNAMES_LIST]
        for file in files:
            if file not in EXCLUDED_FILENAMES_LIST:
                filepath = Path(root) / file
                todos.extend(process_file(filepath))
    return todos


def main():
    start_time = time.perf_counter()

    args = parse_args()

    start_path = Path(args.startpath)
    
    if not start_path.exists():
        print(f'[ERROR] File or directory "{start_path}" does not exist')
        sys.exit(1)
    
    if start_path.is_file():
        found_todos = process_file(start_path)
    else:
        found_todos = process_directory(start_path)

    for todo in found_todos:
        print(todo)

    total_time = time.perf_counter() - start_time
    print('-' * 40 +
          f'\nTotal TODO count: {len(found_todos)} | Time: {total_time * 1000:.3f} ms')


if __name__ == '__main__':
    main()
