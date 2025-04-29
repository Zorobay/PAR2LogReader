from src.gui.abstr.Table import Table, TableModel


class PropertiesTableModel(TableModel):

    def __init__(self, headers):
        super().__init__(headers)


class PropertiesTable(Table):

    def __init__(self):
        super().__init__()
        self._model = PropertiesTableModel(['Key', 'Value'])
        self.setModel(self._model)

    def set_properties(self, properties: dict):
        self.clear_data()

        for key, value in properties.items():
            self._model.append_data([key, str(value)])
