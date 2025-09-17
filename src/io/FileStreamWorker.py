from PyQt6.QtCore import QRunnable, pyqtSlot, QObject, pyqtSignal

from configs import Configs
from src.io.FileStreamer import FileStreamer


class FileStreamWorkerSignals(QObject):
    batch_ready = pyqtSignal(list)


class FileStreamWorker(QRunnable):

    def __init__(self, file_streamer: FileStreamer):
        super().__init__()
        self.signals = FileStreamWorkerSignals()
        self._fs = file_streamer
        self._batch_size = Configs.get_log_read_batch_size()
        self._fs.done_for_now.connect(self._send_incomplete_batch)
        self._batch = []

    @pyqtSlot()
    def run(self):
        for line in self._fs.follow():
            if len(self._batch) >= self._batch_size:
                self.signals.batch_ready.emit(self._batch)
                self._batch = []
            self._batch.append(line)

    def _send_incomplete_batch(self):
        if self._batch:
            self.signals.batch_ready.emit(self._batch)
            self._batch = []
