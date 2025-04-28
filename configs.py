import re
from typing import List, Dict

from PyQt6.QtGui import QColor

DEFAULT_OPEN_DIR = ''
HIGHLIGHTS = []

def read_configs(config: dict):
    global DEFAULT_OPEN_DIR
    DEFAULT_OPEN_DIR = config['default_open_dir']

    global HIGHLIGHTS
    HIGHLIGHTS = config['highlights']

class Configs:

    @classmethod
    def get_default_open_dir(cls):
        return DEFAULT_OPEN_DIR

    @classmethod
    def get_stack_trace_highlights(cls) -> Dict[re.Pattern, QColor]:
        out = dict()
        for regex, color in HIGHLIGHTS['stack_trace'].items():
            pattern = re.compile(regex)
            out[pattern] = QColor(*color)

        return out