import os
import sys
import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg

import qtawesome as qta

from table import TableModel

os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support


class ScaledStyle(qtw.QProxyStyle):
    def __init__(self, base_style, scale):
        super().__init__(base_style)
        self.scale = scale

    def pixelMetric(self, metric, option=None, widget=None):
        value = super().pixelMetric(metric, option, widget)

        if metric in (
            qtw.QStyle.PixelMetric.PM_SmallIconSize,
            qtw.QStyle.PixelMetric.PM_LargeIconSize,
            qtw.QStyle.PixelMetric.PM_ToolBarIconSize,
            qtw.QStyle.PixelMetric.PM_ButtonIconSize,
        ):
            return int(value * self.scale)

        return value
        
class UIScalingManager(qtc.QObject):

    scaleChanged = qtc.Signal(float)
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent = parent)
        
        self.__scale = 1.0
        self.__scaleLB = 1.0
        self.__scaleUB = 1.8
        self.__defaultPixelSize = 15.0
        

    def setScale(self, scale: float, app: qtw.QApplication) -> None:
        self.__scale = scale
        self.applyScale(app)
        self.scaleChanged.emit(self.__scale)

    def applyScale(self, app:qtw.QApplication) -> None:
        font = app.font()
        font.setPointSizeF(10 * self.__scale)
        app.setFont(font)
        
        app.setStyleSheet(f"""
                QWidget{{
                    font-size: {self.__defaultPixelSize * self.__scale}px;
                }}
            """)

        scaledStyle = ScaledStyle(app.style(), self.__scale)
        app.setStyle(scaledStyle)

        # polish toplevel widgets
        for widget in app.topLevelWidgets():
            widget.setFont(app.font())

            mb: qtw.QMenuBar | None = widget.findChild(qtw.QMenuBar)
            if mb:
                mbs = mb.style()
                mbs.unpolish(mb)
                mbs.polish(mb)

                mb.updateGeometry()
                mb.repaint()

                # mb.setFont(app.font())
                # mb.updateGeometry()
                # mb.adjustSize()

    def __clampToScaleRange(self, s: float) -> float:
        return max(self.__scaleLB, min(s, self.__scaleUB))
    
    def scaleUp(self, dx: float, app):
        s = self.__clampToScaleRange(self.__scale + dx)
        self.setScale(s, app)

    def scaleDown(self, dx: float, app):
        s = self.__clampToScaleRange(self.__scale - dx)
        self.setScale(s, app)


class CustomMenuBar(qtw.QMenuBar):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

    def applyScale(self, font: qtg.QFont):
        self.setFont(font)
        self.updateGeometry()
        self.adjustSize()

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qtw.QApplication) -> None:
        super().__init__()

        self.fileMenu = qtw.QMenu("File")
        self.settingsAction: qtg.QAction = self.fileMenu.addAction(qta.icon("msc.gear", color="#00ff00"), "Settings",)
        self.customMenuBar = CustomMenuBar(self)
        self.customMenuBar.addMenu(self.fileMenu)
        self.setMenuBar(self.customMenuBar)

        self.inputField = qtw.QLineEdit("Hello World")
        self.inputLabel = qtw.QLabel("Sample Label")

        self.btnIcon = qta.icon("msc.home", color="#ff00ff")
        self.button = qtw.QPushButton("Sample Button")
        self.button.setIcon(self.btnIcon)

        self.treeWidget = qtw.QTreeWidget()
        self.populateTree(self.treeWidget)

        self.styledButton = qtw.QPushButton("Sample Styled Button")
        self.styledButton.setStyleSheet(f"""
            QPushButton{{ 
                background: orange;
                color: white;
                border: 1px solid black;
                font-size: 25;
                padding: 20px;
                font-weight: bold;
            }}
        """)

        helpAction = qtg.QAction(self)
        helpIcon = qta.icon("msc.question", color="#ff0000")
        helpAction.setIcon(helpIcon)
        helpAction.setToolTip("Help Me")

        self.toolbar = qtw.QToolBar()
        self.toolbar.addSeparator()
        self.toolbar.addAction(helpAction)
        self.toolbar.addSeparator()

        tableModel = TableModel()
        self.tableView = qtw.QTableView()
        self.tableView.setModel(tableModel)

        self.scaleUpButton = qtw.QPushButton("Scale Up")
        self.scaleDownButton = qtw.QPushButton("Scale Down")

        centralLayout = qtw.QVBoxLayout()
        centralLayout.addWidget(self.toolbar)
        centralLayout.addWidget(self.inputLabel)
        centralLayout.addWidget(self.inputField)
        centralLayout.addWidget(self.treeWidget)
        centralLayout.addWidget(self.tableView)
        centralLayout.addWidget(self.button)
        centralLayout.addWidget(self.scaleUpButton)
        centralLayout.addWidget(self.scaleDownButton)
        centralLayout.addWidget(self.styledButton)

        centralWidget = qtw.QFrame()
        centralWidget.setLayout(centralLayout)

        self.setCentralWidget(centralWidget)

        self.app = app
        self.uiScaler = UIScalingManager()

        self.uiScaler.applyScale(self.app)

        self.configure()

    def configure(self):
        self.uiScaler.scaleChanged.connect(self.handleScaleChanged)
        self.scaleUpButton.clicked.connect(lambda: self.uiScaler.scaleUp(0.2, self.app))
        self.scaleDownButton.clicked.connect(lambda: self.uiScaler.scaleDown(0.2, self.app))

    def handleScaleChanged(self, scale: float) -> None:
        self.inputField.setText(f"Scale: {scale}")
        # self.customMenuBar.applyScale(self.app.font())

    @staticmethod
    def populateTree(tree: qtw.QTreeWidget):
        count = 10

        for i in range(count):
            icon = qta.icon("msc.home", color="#ff11ee")
            treeItem = qtw.QTreeWidgetItem(tree)
            treeItem.setIcon(0, icon)
            treeItem.setText(0, f"Icon: {i + 1}")


if __name__ == "__main__":
    qApp = qtw.QApplication(sys.argv)
    qApp.setStyle("Fusion")

    window = MainWindow(qApp)
    window.show()

    sys.exit(qApp.exec())