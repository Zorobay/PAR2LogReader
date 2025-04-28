from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QSplitter, QWidget, QHBoxLayout


class SplitterPainter(QWidget):

    def paintEvent(self, a0):
        painter = QPainter(self)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(Qt.BrushStyle.Dense6Pattern)
        painter.drawRect(self.rect())


class Splitter(QSplitter):

    def __init__(self, direction=Qt.Orientation.Vertical):
        super().__init__(direction)

    def addWidget(self, wdg):
        super().addWidget(wdg)
        self.width = self.handleWidth()
        painter = SplitterPainter()
        painter.setMaximumSize(self.width * 2, self.width * 10)
        layout = QHBoxLayout(self.handle(self.count() - 1))
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(painter)
