from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel


class Icon(QLabel):

    def __init__(self, icon_path: str, width: int=32, height: int=32):
        super().__init__()
        self.pixmap = QPixmap(icon_path)
        self.scaled_pixmap = self.pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio,
                                     Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(self.scaled_pixmap)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)