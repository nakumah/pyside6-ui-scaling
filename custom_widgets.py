import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg


class EditableComboBox(qtw.QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)

        items = [
            {"text": "Item 1", "value": "item1"},
            {"text": "Item 2", "value": "item2"},
            {"text": "Item 3", "value": "item3"},
        ]
        self.setItems(items)

        font = self.font()
        font.setPointSizeF(1.0)

    def setItems(self, items: list[dict[str, str]]):
        self.clear()

        iconColor = f"#f000ff"
        pix = qtg.QPixmap(16, 16)
        pix.fill(qtg.QColor(iconColor))
        icon = qtg.QIcon(pix)

        for item in items:
            self.addItem(item["text"], item["value"])
            self.setItemIcon(self.count() - 1, icon)


class CustomMenuBar(qtw.QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def applyScale(self, font: qtg.QFont):
        self.setFont(font)
        self.updateGeometry()
        self.adjustSize()
