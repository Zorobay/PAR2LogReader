from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from src.gui.Splitter import Splitter
from src.gui.inspector.properties.PropertiesRawTextWidget import PropertiesRawTextWidget
from src.gui.inspector.properties.PropertiesTabWidget import PropertiesTabWidget
from src.gui.inspector.properties.PropertiesTable import PropertiesTable
from src.gui.inspector.stacktrace.StackTraceTabWidget import StackTraceTabWidget
from src.gui.inspector.stacktrace.StackTraceTable import StackTraceTable
from src.gui.inspector.stacktrace.StackTraceTextWidget import StackTraceTextWidget
from src.gui.widgets.HeadingLabel import HeadingLabel
from src.logs import LogLine


class LogInspector(QWidget):

    def __init__(self):
        super().__init__()

        self._layout = QHBoxLayout()
        self._splitter = Splitter(Qt.Orientation.Horizontal)
        self._stack_trace_layout = QVBoxLayout()
        self._properties_layout = QVBoxLayout()

        self._stack_trace_label = HeadingLabel('Stack Trace')
        self._stack_trace_tab = StackTraceTabWidget()
        self._stack_trace_textbox = StackTraceTextWidget()
        self._stack_trace_parsed = StackTraceTable()

        self._properties_label = HeadingLabel('Properties')
        self._properties_tab = PropertiesTabWidget()
        self._properties_raw_text = PropertiesRawTextWidget()
        self._properties_table = PropertiesTable()

        self._initialize()

    def _initialize(self):
        self._stack_trace_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._stack_trace_tab.addTab(self._stack_trace_textbox, 'Text')
        self._stack_trace_tab.addTab(self._stack_trace_parsed, 'Parsed')
        self._stack_trace_layout.addWidget(self._stack_trace_label)
        self._stack_trace_layout.addWidget(self._stack_trace_tab)

        self._properties_tab.addTab(self._properties_table, 'Table')
        self._properties_tab.addTab(self._properties_raw_text, 'Raw Text')
        self._properties_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._properties_layout.addWidget(self._properties_label)
        self._properties_layout.addWidget(self._properties_tab)

        left_widget = QWidget()
        left_widget.setLayout(self._stack_trace_layout)
        self._splitter.addWidget(left_widget)
        right_widget = QWidget()
        right_widget.setLayout(self._properties_layout)
        self._splitter.addWidget(right_widget)
        self._layout.addWidget(self._splitter)
        self.setLayout(self._layout)

    def clear(self):
        self._stack_trace_textbox.clear()
        self._properties_table.clear_data()
        self._stack_trace_parsed.clear_data()

    def inspect(self, line: LogLine):
        self._stack_trace_textbox.setText(line.get_exception_stacktrace())
        self._stack_trace_parsed.set_stack_trace(line.get_exception_stacktrace())

        self._properties_raw_text.set_json(line.get_parsed_json())
        self._properties_table.set_properties(line.get_properties())
