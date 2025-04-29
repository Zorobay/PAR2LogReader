from PyQt6.QtCore import QModelIndex, Qt, QVariant
from PyQt6.QtGui import QColor

from src.gui.abstr.Table import Table, TableModel
from src.logs.LogLine import LogLine, LEVEL_ERROR, LEVEL_WARNING, LEVEL_INFORMATION

DEFAULT_COLOR = QColor().black()
ERROR_COLOR = QColor(255, 0, 0, 50)
WARNING_COLOR = QColor(255, 255, 0, 50)
INFORMATION_COLOR = QColor(0, 255, 0, 50)
LEVEL_COLOR_MAP = {LEVEL_ERROR: ERROR_COLOR, LEVEL_WARNING: WARNING_COLOR, LEVEL_INFORMATION: INFORMATION_COLOR}


class LogTableModel(TableModel):

    def data(self, index: QModelIndex, role: int):
        d = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            match (index.column()):
                case 0:
                    return index.row()
                case 1:
                    return str(d.get_timestamp())
                case 2:
                    return d.get_level()
                case 3:
                    return d.get_message_template()
                case _:
                    return 'ERROR'
        elif role == Qt.ItemDataRole.BackgroundRole:
            if d.get_level() in LEVEL_COLOR_MAP:
                return LEVEL_COLOR_MAP[d.get_level()]
            return DEFAULT_COLOR
        else:
            return QVariant()

    def append_data(self, line: str):
        log_line = LogLine(line)
        super().append_data(log_line)


class LogTable(Table):

    def __init__(self):
        super().__init__()
        self._filepath = None

        self.setModel(LogTableModel(['Row','Timestamp', 'Level', 'Log Message']))
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 100)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.set_bottom_scrolling(True)

    def add_log_line(self, line: str):
        if line and line != '\n':
            self.model().append_data(line)

    def get_selected_line(self) -> LogLine:
        row = self.selectedIndexes()[0].row()
        return self.model().get_row(row)
