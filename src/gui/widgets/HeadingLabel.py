from PyQt6.QtWidgets import QLabel


class HeadingLabel(QLabel):

    def __init__(self, text: str):
        super().__init__(text)

        self.setProperty('class', 'heading')