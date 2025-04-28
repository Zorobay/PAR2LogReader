from PyQt6.QtCore import QRunnable, pyqtSlot

from src.io.FileStreamer import FileStreamer


class FileStreamWorker(QRunnable):

    def __init__(self, filestreamer: FileStreamer, callback):
        super().__init__()
        self._callback = callback
        self._fs = filestreamer

    @pyqtSlot()
    def run(self):
        lines = self._fs.follow()
        for line in lines:
            self._callback(line)