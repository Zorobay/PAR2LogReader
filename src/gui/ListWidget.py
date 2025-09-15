from PyQt6.QtWidgets import QListWidget, QAbstractItemView


class ListWidget(QListWidget):

    def __init__(self, multiple_choice: bool = False):
        super().__init__()

        if multiple_choice:
            self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
