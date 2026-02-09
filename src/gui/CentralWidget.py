from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidgetItem

from src.enums.LogLevel import LogLevel
from src.gui.LogTable import LogTable
from src.gui.Splitter import Splitter
from src.gui.inspector.LogInspector import LogInspector


class CentralWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Widgets
        self.log_table = LogTable()
        self.log_inspector = LogInspector()

        # Layout
        self._splitter = Splitter()
        self._layout = QGridLayout()

        self._initialize()

    def _initialize(self):
        self._splitter.setOrientation(Qt.Orientation.Vertical)
        self._splitter.addWidget(self.log_table)
        self._splitter.addWidget(self.log_inspector)
        self._layout.setSizeConstraint(QGridLayout.SizeConstraint.SetMinimumSize)

        self._layout.addWidget(self._splitter, 0, 0, 1, 1)

        self.setLayout(self._layout)
        self.adjustSize()

        # Signals
        self.log_table.clicked.connect(self._on_log_table_item_clicked)

    def clear(self):
        self.log_table.clear_data()

    def add_log_lines(self, lines: list[str]):
        self.log_table.add_log_lines(lines)

    def _on_log_table_item_clicked(self, item: QTableWidgetItem):
        selected_line = self.log_table.get_selected_line()
        self.log_inspector.inspect(selected_line)

    def filter_log_lines_by_text(self, filter_text: str):
        self.log_table.filter_rows_by_text(filter_text)

    def filter_log_lines_by_log_level(self, log_levels: list[LogLevel]):
        self.log_table.filter_rows_by_log_levels(log_levels)
