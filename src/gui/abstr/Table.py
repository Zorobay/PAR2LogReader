import typing

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, QSortFilterProxyModel, QVariant
from PyQt6.QtGui import QPen, QBrush, QColor
from PyQt6.QtWidgets import QHeaderView, QTableView, QStyledItemDelegate, QStyle


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


class OutlineSelectedRowDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        # Call the default paint method first
        super().paint(painter, option, index)

        # Get the background color from your model
        model_background = index.data(Qt.ItemDataRole.BackgroundRole)

        # Check if the item is selected
        is_selected = option.state & QStyle.StateFlag.State_Selected

        # If selected, and we have a model background color, use it
        if is_selected and model_background is not None and not isinstance(model_background, QVariant):
            # Save painter state
            painter.save()

            # Set pen for outline
            pen = QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine)
            painter.setPen(pen)

            # Draw outline around the cell
            rect = option.rect
            painter.drawRect(rect.adjusted(1, 1, -1, -1))

            # Restore background color from TableModel
            if isinstance(model_background, QColor):
                option.backgroundBrush = QBrush(model_background)
            else:
                option.backgroundBrush = QBrush(QColor(model_background))
            # Remove the selected state to prevent default selection styling
            option.state &= ~QStyle.StateFlag.State_Selected

            # Restore painter state
            painter.restore()


class Table(QTableView):

    def __init__(self):
        super().__init__()
        self._scroll_to_bottom = False
        self._sort_filter_proxy_model = QSortFilterProxyModel()
        self._source_model = None

        self.setItemDelegate(OutlineSelectedRowDelegate())
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)

    def setModel(self, model: TableModel):
        self._source_model = model
        self._sort_filter_proxy_model.setSourceModel(self._source_model)
        self._sort_filter_proxy_model.setFilterKeyColumn(-1)
        self._sort_filter_proxy_model.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        super().setModel(self._sort_filter_proxy_model)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSectionResizeMode(self.model().columnCount(), QHeaderView.ResizeMode.Stretch)
        self.setSortingEnabled(True)

    def set_bottom_scrolling(self, enabled: bool):
        self._scroll_to_bottom = enabled

    def model(self) -> TableModel:
        return self._source_model

    def clear_data(self):
        self.model().clear_data()

    def rowsInserted(self, parent, start, end):
        if self._scroll_to_bottom:
            self.scrollToBottom()

    def selectedIndexes(self) -> list[QModelIndex]:
        indices = super().selectedIndexes()
        return [self._sort_filter_proxy_model.mapToSource(index) for index in indices]

    def filter_rows(self, filter_str: str):
        self._sort_filter_proxy_model.setFilterFixedString(filter_str)

    def resize_columns_to_content(self, max_width: int):
        self.resizeColumnsToContents()
        num_cols = self.model().columnCount()
        for col_i in range(num_cols):
            col_width = self.columnWidth(col_i)
            if col_width > max_width:
                self.setColumnWidth(col_i, max_width)
