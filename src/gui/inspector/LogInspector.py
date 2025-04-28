from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from src.gui.Splitter import Splitter
from src.gui.inspector.PropertiesTable import PropertiesTable
from src.gui.inspector.StackTraceWidget import StackTraceWidget
from src.logs import LogLine


class LogInspector(QWidget):

    def __init__(self):
        super().__init__()
        self._mono_font = QFont('Consolas')

        self._layout = QHBoxLayout()
        self._splitter = Splitter(Qt.Orientation.Horizontal)
        self._stack_trace_layout = QVBoxLayout()
        self._properties_layout = QVBoxLayout()

        self._stack_trace_label = QLabel('Stack Trace')
        self._stack_trace_textbox = StackTraceWidget()

        self._properties_label = QLabel('Properties')
        self._properties_table = PropertiesTable()

        self._initialize()

    def _initialize(self):
        self._stack_trace_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._stack_trace_layout.addWidget(self._stack_trace_label)
        self._stack_trace_textbox.setFont(self._mono_font)
        self._stack_trace_layout.addWidget(self._stack_trace_textbox)

        self._properties_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._properties_layout.addWidget(self._properties_label)
        self._properties_layout.addWidget(self._properties_table)

        left_widget = QWidget()
        left_widget.setLayout(self._stack_trace_layout)
        self._splitter.addWidget(left_widget)
        right_widget = QWidget()
        right_widget.setLayout(self._properties_layout)
        self._splitter.addWidget(right_widget)
        self._layout.addWidget(self._splitter)
        self.setLayout(self._layout)

    def inspect(self, line: LogLine):
        self._stack_trace_textbox.setText(line.get_exception_stacktrace())
        self._properties_table.set_properties(line.get_properties())
