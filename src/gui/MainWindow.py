from pathlib import Path

from PyQt6.QtCore import QThreadPool
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QPushButton, QFileDialog, QStatusBar, QToolBar

from configs import Configs
from src.gui.CentralWidget import CentralWidget
from src.io.FileStreamWorker import FileStreamWorker
from src.io.FileStreamer import FileStreamer
import configs


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

        # === Widgets ===
        self._button_tool_bar = QToolBar()
        self.open_button = QPushButton('Open')

        self._initialize()
        self._signals()

    def _initialize(self):
        self.setWindowTitle('PAR2 Log Reader')
        self.resize(1300, 600)

        self.setCentralWidget(self.central_widget)
        self.setStatusBar(self.status_bar)

        # === Toolbar ===
        self._button_tool_bar.addWidget(self.open_button)

        # === Layouts ===
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self._button_tool_bar)

    def _signals(self):
        self.open_button.clicked.connect(self._on_open_button_clicked)

    def _on_open_button_clicked(self):
        self._filepath, _ = QFileDialog.getOpenFileName(self, 'Open File', str(self._last_open_dir),
                                                        'Log Files (*.log)')

        if self._filepath:
            self._last_open_dir = Path(self._filepath).parent

            print(f'Opening log at: {self._filepath}')

            self.status_bar.showMessage(self._filepath)
            self._read_file_and_populate_table()

    def _read_file_and_populate_table(self):
        file_streamer = FileStreamer(self._filepath, 2000)
        worker = FileStreamWorker(file_streamer, self._on_log_line_read)
        self._threadpool.start(worker)

    def _on_log_line_read(self, log_line: str):
        if log_line and log_line.strip() != '\n':
            self.central_widget.add_log_line(log_line)
