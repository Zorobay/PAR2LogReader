import re
from typing import Dict, List

from PyQt6.QtGui import QSyntaxHighlighter, QColor, QBrush, QTextCharFormat
from PyQt6.QtWidgets import QTextEdit

from configs import Configs


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
                self.setFormat(match.start(), match.end()-match.start(), fmt)
                start = match.end()

        self.setCurrentBlockState(0)


class StackTraceWidget(QTextEdit):

    def __init__(self):
        super().__init__()

        self._syntax_highlighter = SyntaxHighlighter(Configs.get_stack_trace_highlights(), self)
