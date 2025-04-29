import typing
from doctest import script_from_examples

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt6.QtWidgets import QHeaderView, QTableView


class TableModel(QAbstractTableModel):

    def __init__(self, headers: typing.List[str]):
        super().__init__()
        self._data = []
        self._headers = headers

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, parent=None) -> int:
        return len(self._headers)

    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]

    def data(self, index, role):
        row = self._data[index.row()]
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
            return row[index.column()]

    def get_row(self, index: int) -> typing.Any:
        return self._data[index]

    def append_data(self, data):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(data)
        self.endInsertRows()

    def clear_data(self):
        self.beginResetModel()
        self._data = []
        self.endResetModel()


class Table(QTableView):

    def __init__(self):
        super().__init__()
        self._scroll_to_bottom = False

    def setModel(self, model: TableModel):
        super().setModel(model)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(self.model().columnCount(), QHeaderView.ResizeMode.Stretch)
        self.setSortingEnabled(True)

    def set_bottom_scrolling(self, enabled: bool):
        self._scroll_to_bottom = enabled

    def model(self) -> TableModel:
        return super().model()

    def clear_data(self):
        self.model().clear_data()

    def rowsInserted(self, parent, start, end):
        if self._scroll_to_bottom:
            self.scrollToBottom()