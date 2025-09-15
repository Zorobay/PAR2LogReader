import re
import typing

from PyQt6.QtCore import QModelIndex, Qt, QVariant
from PyQt6.QtGui import QFont

from src.gui.abstr.Table import Table, TableModel

REG_AT = re.compile(r'\n+\s+at')
REG_LINE = re.compile(r':line (\d+)')
REG_CLASS_METHOD = re.compile(r'^DPA.PAR2.[\w+\.]+\.(\w+)\.(\w+(?:\[\w\])?\([\w\s,]+\))', re.DOTALL)
MONO_FONT = QFont('Consolas')


class StackTraceTableModel(TableModel):

    def data(self, index: QModelIndex, role: int):
        d = self._data[index.row()]
        if role == Qt.ItemDataRole.FontRole:
            match (index.column()):
                case 0: return MONO_FONT

        if role == Qt.ItemDataRole.DisplayRole:
            return str(d[index.column()])
        else:
            return QVariant()


def _parse_stack_trace(stack_trace: str) -> typing.List[typing.List[str]]:
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


class StackTraceTable(Table):

    def __init__(self):
        super().__init__()
        self._columns = ['Depth', 'Class', 'Method', 'Line']
        self._max_col_width = 400
        self.setModel(StackTraceTableModel(self._columns))
        self.setColumnWidth(0, 80)
        # self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        # self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.verticalHeader().setVisible(False)

        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.setMouseTracking(True)

    def set_stack_trace(self, stack_trace: str):
        self.clear_data()
        data = _parse_stack_trace(stack_trace)
        for i, d in enumerate(data):
            row = [i]
            row.extend(d)
            self.model().append_data(row)

        self.resize_columns_to_content(self._max_col_width)
