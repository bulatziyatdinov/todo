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
    '.idea',
    '.vscode',
    '.ruff_cache',
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


def error(content: str, crash: bool = False) -> None:
    print(f'[ERROR] {content}')
    if crash:
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Search for TODO comments in files.",
        add_help=True
    )
    parser.add_argument('startpath', nargs='?', default='.',
                        help="Path to file or directory (default: current directory)")
    parser.add_argument('-i', '--ignore-case', action='store_true',
                        help="Enable ignoring case")
    return parser.parse_args()


def find_prefix(prefix: bytes, line: bytes, ignore_case: bool = False) -> bool:
    # Changing the value of a variable every time is not a good idea.
    if ignore_case:
        prefix = prefix.lower()
        line = line.lower()
    return prefix in line


def process_file(filepath: Path, ignore_case: bool = False) -> list[TodoInfo]:
    todos = []
    try:
        with open(filepath, 'rb') as f:
            file_text = f.readlines()
        for num, line in enumerate(file_text, 1):
            if find_prefix(TODO_PREFIX, line, ignore_case):
                todos.append(TodoInfo(filepath, num, line))
    except OSError:
        error(f'Could not read file "{filepath}"')
    return todos


def process_directory(root_path: Path, ignore_case: bool = False) -> list[TodoInfo]:
    todos = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERNAMES_LIST]
        for file in files:
            if file not in EXCLUDED_FILENAMES_LIST:
                filepath = Path(root) / file
                todos.extend(process_file(filepath, ignore_case))
    return todos


def main():
    start_time = time.perf_counter()

    args = parse_args()

    start_path = Path(args.startpath)
    
    if not start_path.exists():
        error(f'File or directory "{start_path}" does not exist', True)
    
    if start_path.is_file():
        found_todos = process_file(start_path, args.ignore_case)
    else:
        found_todos = process_directory(start_path, args.ignore_case)

    for todo in found_todos:
        print(todo)

    total_time = time.perf_counter() - start_time
    print(('-' * 40 + '\n')* (len(found_todos) > 0) +
          f'Total TODO count: {len(found_todos)} | Time: {total_time * 1000:.3f} ms')


if __name__ == '__main__':
    main()
