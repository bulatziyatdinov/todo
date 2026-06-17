#!/usr/bin/env python3

import os
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


def main():
    found_todos = []
    error_list = []
    
    start_path = '.'
    start_time = time.perf_counter()
    
    for root, dirs, files in os.walk(start_path):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_FOLDERNAMES_LIST]
        
        for file in files:
            if file not in EXCLUDED_FILENAMES_LIST:
                filepath = Path(root) / file
                try:
                    with open(filepath, 'rb') as f:
                        file_text = f.readlines()

                    for num, line in enumerate(file_text, 1):
                        if TODO_PREFIX in line:
                            found_todos.append(TodoInfo(filepath, num, line))

                except OSError:
                    error_list.append(f"Can't read '{filepath}")


    total_time = time.perf_counter() - start_time

    print(f"Total TODO count: {len(found_todos)} | Time: {total_time * 1000:.3f} ms\n"
          + '-' * 40)
    for todo in found_todos:
        print(todo)


if __name__ == '__main__':
    main()
