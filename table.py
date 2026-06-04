import pandas as pd
import numpy as np
from PySide6.QtCore import QAbstractTableModel, Qt


class TableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)

        entries = np.random.rand(70, 4) * 100
        colNames = [f"Column {i + 1 }\n(x/y)" for i in range(entries.shape[1])]
        self._df = pd.DataFrame(
            entries,
            columns=colNames,
        )

    def data(self, index, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            value = self._df.iloc[index.row(), index.column()]
            return f"{float(value):,.3f}"
        return None

    def rowCount(self, parent=None):
        return self._df.shape[0]

    def columnCount(self, /, parent= ...):
        return self._df.shape[1]

    def headerData(self, section, orientation, /, role = ...):
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
                return str(section + 1)
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
                return str(self._df.columns[section])
        return None