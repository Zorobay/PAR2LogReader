import re
import typing

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView

REG_AT = re.compile(r'\n+\s+at')
REG_LINE = re.compile(r':line (\d+)')
REG_CLASS_METHOD = re.compile(r'^DPA.PAR2.[\w+\.]+\.(\w+)\.(\w+\([\w\s,]+\))', re.DOTALL)
MONO_FONT = QFont('Consolas')

def monofont_item(value: typing.Any) -> QTableWidgetItem:
    item = QTableWidgetItem(str(value))
    item.setFont(MONO_FONT)
    return item
class StackTraceParsedWidget(QTableWidget):

    def __init__(self):
        super().__init__()
        self._columns = ['Depth', 'Class', 'Method', 'Line']
        self.setColumnCount(len(self._columns))
        self.setHorizontalHeaderLabels(self._columns)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setVisible(False)

    def set_stack_trace(self, stack_trace: str):
        data = self._parse_stack_trace(stack_trace)
        for i, d in enumerate(data):
            row_num = self.rowCount()
            self.insertRow(row_num)
            self.setItem(row_num, 0, QTableWidgetItem(str(i)))
            self.setItem(row_num, 1, monofont_item(d[0]))
            self.setItem(row_num, 2, monofont_item(d[1]))
            self.setItem(row_num, 3, QTableWidgetItem(d[2]))

    def _parse_stack_trace(self, stack_trace: str) -> typing.List[typing.List[str]]:
        out = []
        at_split = [l.strip() for l in REG_AT.split(stack_trace)]

        for row in at_split:
            cm_match = REG_CLASS_METHOD.match(row)
            line_match = REG_LINE.search(row)
            if cm_match and line_match:
                clazz = cm_match.group(1)
                method = cm_match.group(2)
                line = line_match.group(1)
                out.append([clazz, method, line])

        return out
