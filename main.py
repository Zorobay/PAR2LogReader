import json
import sys

from PyQt6.QtWidgets import QApplication

from src.config import configs
from src.gui.MainWindow import MainWindow


def read_configs():
    with open('config/main.json', 'r') as f:
        config = json.load(f)
        configs.read_configs(config)


def read_stylesheet(app: QApplication):
    with open('res/style.qss', 'r') as f:
        app.setStyleSheet(f.read())


if __name__ == '__main__':
    try:
        read_configs()
        app = QApplication(sys.argv)
        read_stylesheet(app)
        window = MainWindow()
        window.show()
        app.exec()
    except BaseException as e:
        print(e)
