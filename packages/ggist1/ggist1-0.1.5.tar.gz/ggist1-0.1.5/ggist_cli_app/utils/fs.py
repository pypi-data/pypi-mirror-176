import os
from pathlib import Path
from typing import Sequence

def exists(path)->bool:
    return os.path.exists(path)

def mkdir(dir):
    Path(dir).mkdir(parents=True, exist_ok=True)

def touch(file):
    Path(file).touch()

def file_read_lines(file) -> Sequence[str]:
    with open(file, 'r') as fp:
        return map(lambda s: s.strip(), fp.readlines())

def file_write_lines(file, lines):
    with open(file, 'w') as fp:
        fp.writelines(map(lambda s: f'{s}\n', lines))