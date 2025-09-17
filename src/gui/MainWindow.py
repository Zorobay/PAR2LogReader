from pathlib import Path

from PyQt6.QtCore import QThreadPool
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QStatusBar, QToolBar, QLineEdit, QLabel

from configs import Configs
from src.gui.CentralWidget import CentralWidget
from src.gui.Icon import Icon
from src.io.FileStreamWorker import FileStreamWorker
from src.io.FileStreamer import FileStreamer


class StatusBar(QStatusBar):
    def __init__(self):
        super().__init__()
        self._status_bar_right_widget = QLabel()
        self.addPermanentWidget(self._status_bar_right_widget)

    def show_message_right_side(self, msg: str):
        self._status_bar_right_widget.setText(msg)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # === Data ===
        self._last_open_dir = Configs.get_default_open_dir()
        self._filepath = None
        self._threadpool = QThreadPool()

        # === Layout ===
        self.central_widget = CentralWidget()

        # === Status bar ===
        self.status_bar = StatusBar()

        # === Menubar ===
        self._menu_bar = self.menuBar()

        # === Toolbar ===
        self._button_tool_bar = QToolBar()
        self._filter_icon = Icon('res/icons/filter.png', 28, 28)
        self._search_input = QLineEdit()
        # self._filter_log_level =

        self._initialize()

    def _initialize(self):
        self.setWindowTitle('PAR2 Log Reader')
        self.resize(1600, 800)

        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)

        # === Menu ===
        file_menu = self._menu_bar.addMenu('File')
        open_action = QAction('Open', self)
        open_action.triggered.connect(self._on_open_button_clicked)
        file_menu.addAction(open_action)

        # === Toolbar ===
        self._button_tool_bar.addWidget(self._search_input)
        self._search_input.textChanged.connect(self._on_search_input_text_changed)

        # === Layouts ===
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self._button_tool_bar)

    def _on_open_button_clicked(self):
        self._filepath, _ = QFileDialog.getOpenFileName(self, 'Open File', str(self._last_open_dir),
                                                        'Log Files (*.log)')

        if self._filepath:
            self._last_open_dir = Path(self._filepath).parent

            print(f'Opening log at: {self._filepath}')

            self.status_bar.showMessage(self._filepath)
            self.central_widget.clear()
            self._read_file_and_populate_table()

    def _on_search_input_text_changed(self):
        text = self._search_input.text()
        self.central_widget.filter_log_lines(text)
        self._update_row_count_status()

    def _read_file_and_populate_table(self):
        file_streamer = FileStreamer(self._filepath, Configs.get_log_read_frequency_ms())
        worker = FileStreamWorker(file_streamer)
        worker.signals.batch_ready.connect(self._on_log_line_read)
        self._threadpool.start(worker)

    def _update_row_count_status(self):
        row_count = self.central_widget.log_table.row_count()
        filtered_row_count = self.central_widget.log_table.filtered_row_count()
        self.status_bar.show_message_right_side(f'{filtered_row_count} of {row_count} lines')

    def _on_log_line_read(self, log_lines: list[str]):
        self.central_widget.add_log_lines(log_lines)
        self._update_row_count_status()
