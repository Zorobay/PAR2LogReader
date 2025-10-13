from PyQt6.QtWidgets import QLabel


class HeadingLabelWidget(QLabel):

    def __init__(self, text: str):
        super().__init__(text)

        self.setProperty('class', 'heading')
