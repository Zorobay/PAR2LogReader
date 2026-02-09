import json
import re
from typing import Dict

from PyQt6.QtGui import QSyntaxHighlighter, QColor, QBrush, QTextCharFormat, QFont
from PyQt6.QtWidgets import QTextEdit

from src.config.configs import Configs


def create_format(color: QColor) -> QTextCharFormat:
    brush = QBrush(color)
    fmt = QTextCharFormat()
    fmt.setForeground(brush)
    return fmt


class SyntaxHighlighter(QSyntaxHighlighter):

    def __init__(self, highlights: Dict[re.Pattern, QColor], parent=None):
        super().__init__(parent)

        self._highlights = highlights

    def highlightBlock(self, text):
        for regex, color in self._highlights.items():
            fmt = create_format(color)
            start = 0

            while match := regex.search(text, start):
                self.setFormat(match.start(), match.end() - match.start(), fmt)
                start = match.end()

        self.setCurrentBlockState(0)


class PropertiesRawTextWidget(QTextEdit):

    def __init__(self):
        super().__init__()
        self._mono_font = QFont('Consolas')
        self._syntax_highlighter = SyntaxHighlighter(Configs.get_json_highlights(), self)
        self.setFont(self._mono_font)

    def set_json(self, jsn: dict):
        json_pretty = json.dumps(jsn, indent=2)
        self.setText(json_pretty)
