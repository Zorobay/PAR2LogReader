import re
from typing import Dict, Any

from PyQt6.QtGui import QColor

DEFAULT_OPEN_DIR = ''
HIGHLIGHTS = []
LOG_READ_BATCH_SIZE = 200
LOG_READ_FREQUENCY_MS = 4000  # reads every n milliseconds


def _read_or_default(config: dict, key: str, default: Any) -> Any:
    if key in config:
        return config[key]
    else:
        return default


def read_configs(config: dict):
    global DEFAULT_OPEN_DIR
    DEFAULT_OPEN_DIR = _read_or_default(config, 'default_open_dir', DEFAULT_OPEN_DIR)

    global HIGHLIGHTS
    HIGHLIGHTS = _read_or_default(config, 'highlights', HIGHLIGHTS)

    global LOG_READ_BATCH_SIZE
    LOG_READ_BATCH_SIZE = _read_or_default(config, 'log_read_batch_size', LOG_READ_BATCH_SIZE)

    global LOG_READ_FREQUENCY_MS
    LOG_READ_FREQUENCY_MS = _read_or_default(config, 'log_read_frequency_ms', LOG_READ_FREQUENCY_MS)


class Configs:

    @classmethod
    def get_log_read_batch_size(cls) -> int:
        return LOG_READ_BATCH_SIZE

    @classmethod
    def get_default_open_dir(cls) -> str:
        return DEFAULT_OPEN_DIR

    @classmethod
    def get_log_read_frequency_ms(cls) -> int:
        return LOG_READ_FREQUENCY_MS

    @classmethod
    def get_stack_trace_highlights(cls) -> Dict[re.Pattern, QColor]:
        return cls._get_highlights('stack_trace')

    @classmethod
    def get_json_highlights(cls) -> Dict[re.Pattern, QColor]:
        return cls._get_highlights('json')

    @classmethod
    def _get_highlights(cls, name: str) -> Dict[re.Pattern, QColor]:
        out = dict()
        for regex, color in HIGHLIGHTS[name].items():
            pattern = re.compile(regex)
            out[pattern] = QColor(*color)

        return out
