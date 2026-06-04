import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

import resources.styling as sty

from utils.scaling import GUI_SCALER


class CustomMenuBar(qtw.QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def applyScale(self, font: qtg.QFont):
        self.setFont(font)
        self.updateGeometry()
        self.adjustSize()


class VLabel(qtw.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__setQss()

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)

    def __setQss(self):
        self.setObjectName("VLabel")
        sty.setStyleSheet(self, "q_label")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VLineEdit(qtw.QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)

        self.__setQss()

    def __setQss(self):
        self.setObjectName("VLineEdit")
        sty.setStyleSheet(self, "q_line_edit")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VTextEdit(qtw.QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)

        self.__setQss()

    def __setQss(self):
        self.setObjectName("VTextEdit")
        sty.setStyleSheet(self, "q_text_edit")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VPushButton(qtw.QPushButton):
    def __init__(self, *args, variantPairs: list[tuple[str, str]] = [], **kwargs):
        super().__init__(*args, **kwargs)

        self._variantPairs = variantPairs

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)

        self.__setQss()

    def __setQss(self):
        self.setObjectName("VPushButton")

        for variantId, variantIdValue in self._variantPairs:
            self.setProperty(variantId, variantIdValue)

        sty.setStyleSheet(self, "q_push_button")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VCheckBox(qtw.QCheckBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)
        self.__setQss()

    def __setQss(self):
        self.setObjectName("VCheckBox")
        sty.setStyleSheet(self, "q_check_box")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VComboBox(qtw.QComboBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # bugfix: styling components need the item delegate to override system style
        self.setItemDelegate(qtw.QStyledItemDelegate())
        GUI_SCALER.scaleChanged.connect(self.__handleScaleChanged)
        self.__setQss()

    def __setQss(self):
        self.setObjectName("VComboBox")
        sty.setStyleSheet(self, "q_combo_box")

        self.setStyle(qtw.QApplication.style())
        qtw.QApplication.processEvents()

    def __updateFont__(self, scale: float):

        # update the font
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)

    def __updateIconSize__(self):
        # udpate the icons
        fm = qtg.QFontMetrics(self.font())
        size = fm.ascent()
        self.setIconSize(qtc.QSize(size, size))

    def __handleScaleChanged(self, scale: float):
        self.__updateFont__(scale)
        self.__updateIconSize__()


class VProgressBar(qtw.QProgressBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__setQSS()

    def __setQSS(self):
        self.setObjectName("VProgressBar")
        sty.setStyleSheet(self, "q_progress_bar")


class VSlider(qtw.QSlider):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__setQSS()

    def __setQSS(self):
        self.setObjectName("VSlider")
        sty.setStyleSheet(self, "q_slider")


class VTreeWidget(qtw.QTreeWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)
        self.__setQSS()

    def __setQSS(self):
        self.setObjectName("VTreeWidget")
        sty.setStyleSheet(self, "q_tree_widget")

    def __updateFont__(self, scale: float):

        # update the font
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


class VTableView(qtw.QTableView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        GUI_SCALER.scaleChanged.connect(self.__updateFont__)
        self.__setQSS()

    def __setQSS(self):
        self.setObjectName("VTableView")
        sty.setStyleSheet(self, "q_table_widget")

    def __updateFont__(self, scale: float):

        # update the font
        font = self.font()
        font.setPointSizeF(GUI_SCALER.baseFontSize() * scale)
        self.setFont(font)


