from pathlib import Path

from PyQt6.QtCore import QThreadPool
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMainWindow, QFileDialog, QStatusBar, QToolBar, QLineEdit

from configs import Configs
from src.gui.CentralWidget import CentralWidget
from src.gui.Icon import Icon
from src.io.FileStreamWorker import FileStreamWorker
from src.io.FileStreamer import FileStreamer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # === Data ===
        self._last_open_dir = Configs.get_default_open_dir()
        self._filepath = None
        self._threadpool = QThreadPool()

        # === Layout ===
        self.central_widget = CentralWidget()
        self.status_bar = QStatusBar()

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


    def _read_file_and_populate_table(self):
        file_streamer = FileStreamer(self._filepath, 2000)
        worker = FileStreamWorker(file_streamer, self._on_log_line_read)
        self._threadpool.start(worker)

    def _on_log_line_read(self, log_line: str):
        if log_line and log_line.strip() != '\n':
            self.central_widget.add_log_line(log_line)
