#!/usr/bin/env python3

import argparse
import os
import sys
import time
from pathlib import Path

TODO_PREFIX = b'TODO:'

DEFAULT_EXCLUDED_FOLDERS = {
    # IDE stuff
    '.idea', '.vscode',
    # Cache
    '__pycache__', '.ruff_cache', '.pytest_cache', '.mypy_cache',
    # venvs
    '.venv', 'venv', '.env', 'env',
    # Other
    '.git', 'build', 'dist', 'bin', '.DS_Store',
}

DEFAULT_EXCLUDED_FILES = {
    '.env', '.env.local', '.env.test',
    '.gitignore',
}

DEFAULT_EXCLUDED_EXTENSIONS = {
    # Text
    '.pdf', '.md', '.txt', '.log',
    # Data sources
    '.json', '.csv', '.docx', '.doc', '.xlsx',  '.xls',
    # Databases
    '.db', '.sqlite3',
    # Media
    '.mp4', '.avi', '.mov', '.mkv',
    '.mp3', '.wav', '.ogg',
    '.png', '.jpeg', '.jpg', '.svg', '.ico', '.bmp',
    # Other
    '.env',
    '.lock',
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz', '.tgz', '.zst',
    '.temp', '.tmp',
    '.pickle', '.pkl',
    '.dat',
    '.bin', '.exe', '.dll', '.so',
}


class TodoInfo:
    __slots__ = ['filepath', 'line_number', 'line_str']
    def __init__(self, filepath: Path, line_number: int, line_str: bytes):
        self.filepath = filepath
        self.line_number = line_number
        self.line_str = line_str

    def __str__(self):
        return (f'{self.filepath}:{self.line_number} -> '
                f'{self.line_str.strip().decode('utf-8', errors='replace')}')


def error(content: str, crash: bool = False) -> None:
    print(f'[ERROR] {content}')
    if crash:
        sys.exit(1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Search for TODO comments in files',
        add_help=True
    )
    parser.add_argument(
        'path',
        nargs='?',
        default='.',
        help='Path to file or directory (default: current directory)'
    )
    parser.add_argument(
        '-i',
        '--ignore-case',
        action='store_true',
        help='Ignores the case of text in the file and the prefix'
    )
    parser.add_argument(
        '-xf',
        '--exclude-files',
        nargs='+',
        help='List of file names to exclude from search. Example: error.log notes.txt'
    )
    parser.add_argument(
        '-xd',
        '--exclude-dirs',
        nargs='+',
        help='List of directory names to exclude from search. Example: tests data'
    )
    parser.add_argument(
        '-xe',
        '--exclude-extensions',
        nargs='+',
        help='List of file extensions to exclude from search. Example: .pdf .txt'
    )
    parser.add_argument(
        '-xo',
        '--exclude-default-off',
        action='store_true',
        help='Disable built-in default exclusions for files, directories and extensions'
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


def process_directories(root_path: Path, settings: dict) -> list[TodoInfo]:
    todos = []
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in settings['excluded_folders']]
        for file in files:
            if (file not in settings['excluded_files']) \
                    and (Path(file).suffix not in settings['excluded_extensions']):
                filepath = Path(root) / file
                todos.extend(process_file(filepath, settings))
    return todos


def process_settings(args: argparse.Namespace) -> dict:
    if args.exclude_default_off:
        excluded_folders = set()
        excluded_files = set()
        excluded_extensions = set()
    else:
        excluded_folders = DEFAULT_EXCLUDED_FOLDERS
        excluded_files = DEFAULT_EXCLUDED_FILES
        excluded_extensions = DEFAULT_EXCLUDED_EXTENSIONS

    if args.exclude_dirs is not None:
        excluded_folders |= set(args.exclude_dirs)
    if args.exclude_files is not None:
        excluded_files |= set(args.exclude_files)
    if args.exclude_extensions is not None:
        excluded_extensions |= set(args.exclude_extensions)

    return {
        'path': args.path,
        'ignore_case': args.ignore_case,
        'todo_prefix': TODO_PREFIX.lower() if args.ignore_case else TODO_PREFIX,
        'excluded_folders': excluded_folders,
        'excluded_files': excluded_files,
        'excluded_extensions': excluded_extensions,
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
        found_todos = process_directories(start_path, settings)

    print('\n'.join(map(str, found_todos)) + '\n' * (len(found_todos) > 0), end='')

    total_time = time.perf_counter() - start_time
    print(('-' * 40 + '\n') * (len(found_todos) > 0) +
          f'Total TODO count: {len(found_todos)} | Time: {total_time * 1000:.3f} ms')


if __name__ == '__main__':
    main()
