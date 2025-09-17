from PyQt6.QtCore import QModelIndex, Qt, QVariant, QSortFilterProxyModel
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

    def extend_data(self, lines: list[str]):
        log_lines = [LogLine(line) for line in lines]
        super().extend_data(log_lines)

class LogLineFilterProxyModel(QSortFilterProxyModel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._filter_str = None

    def set_filter_str(self, filter_str: str):
        self._filter_str = filter_str
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source_model = self.sourceModel()
        log_line = source_model.get_row(source_row)
        line = log_line.get_original_line()
        if not self._filter_str:
            return True

        return self._filter_str.lower() in line.lower()

class LogTable(Table):

    def __init__(self):
        super().__init__()
        self._filepath = None
        self._sort_filter_proxy_model = LogLineFilterProxyModel()

        self.setModel(LogTableModel(['Row', 'Timestamp', 'Level', 'Log Message']), self._sort_filter_proxy_model)
        self.setColumnWidth(0, 60)
        self.setColumnWidth(1, 200)
        self.setColumnWidth(2, 100)
        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.set_bottom_scrolling(True)
        self.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    def filter_rows(self, filter_str: str):
        self._proxy_model.set_filter_str(filter_str)

    def add_log_lines(self, lines: list[str]):
        actual_lines = [l for l in lines if l and l != '\n']
        self.model().extend_data(actual_lines)

    def get_selected_line(self) -> LogLine:
        row = self.selectedIndexes()[0].row()
        return self.model().get_row(row)
