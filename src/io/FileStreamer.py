import os
import time
from pathlib import Path
from typing import Generator


class FileStreamer:

    def __init__(self, filepath: Path, update_freq_ms: int):
        self._filepath = filepath
        self._update_freq_ms = update_freq_ms

    def follow(self) -> Generator[str]:
        with open(self._filepath, 'r') as f:
            f.seek(0, os.SEEK_SET)
            while True:
                line = f.readline()
                print(f"Reading line from file: {line}")
                if not line:
                    time.sleep(self._update_freq_ms / 1000)
                    continue
                yield line