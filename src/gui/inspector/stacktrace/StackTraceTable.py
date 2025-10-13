import re
import typing

from PyQt6.QtCore import QModelIndex, Qt, QVariant
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QHeaderView

from src.gui.abstr.Table import Table, TableModel

REG_STACKTRACE_SPLIT = re.compile(r"at\s(.*)\sin(.*):line\s(\d+)")
REG_FILE = re.compile(r".*\\(.*)")
REG_METHOD = re.compile(r".*\.(\w+)\(.*")
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
    file_locations = REG_STACKTRACE_SPLIT.findall(stack_trace)

    for full_method, file, line in file_locations:
        filename_match = REG_FILE.match(file)
        method_match = REG_METHOD.match(full_method)

        if filename_match and method_match:
            filename = filename_match.group(1)
            method = method_match.group(1)
            line = int(line)
            out.append([filename, method, line])

    return out


class StackTraceTable(Table):

    def __init__(self):
        super().__init__()
        self._columns = ['Depth', 'Class', 'Method', 'Line']
        self._max_col_width = 400
        self.setModel(StackTraceTableModel(self._columns))

        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 80)
        self.setColumnWidth(3, 80)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(False)

        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.setMouseTracking(True)

    def set_stack_trace(self, stack_trace: str):
        self.clear_data()
        data = _parse_stack_trace(stack_trace)
        self.model().extend_data([[i, *d] for i, d in enumerate(data)])
