import os
import time
from pathlib import Path
from typing import Generator

from PyQt6.QtCore import QObject, pyqtSignal


class FileStreamer(QObject):
    done_for_now = pyqtSignal(bool)

    def __init__(self, filepath: Path, update_freq_ms: int):
        super().__init__()
        self._filepath = filepath
        self._update_freq_ms = update_freq_ms

    def follow(self) -> Generator[str]:
        with open(self._filepath, 'r') as f:
            f.seek(0, os.SEEK_SET)
            while True:
                line = f.readline()
                print(f"Reading line from file: {line}")
                if not line:
                    self.done_for_now.emit(True)
                    time.sleep(self._update_freq_ms / 1000)
                    continue
                yield line
