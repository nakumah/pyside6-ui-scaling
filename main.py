import os
import sys
import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg

import qtawesome as qta

from table import TableModel
from scaling import GUIScalingManager


os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support


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
        self.scaleUpButton = qtw.QPushButton("Scale Up")
        self.scaleDownButton = qtw.QPushButton("Scale Down")

        scrollAreaLayout = qtw.QVBoxLayout()
        for w in MainWindow.createGroupWidgets(100):
            scrollAreaLayout.addWidget(w)

        scrollAreaWidget = qtw.QWidget()
        scrollAreaWidget.setLayout(scrollAreaLayout)

        centralScrollArea = qtw.QScrollArea()
        centralScrollArea.setWidgetResizable(True)
        centralScrollArea.setWidget(scrollAreaWidget)

        widgetScalingBtnsLayout = qtw.QVBoxLayout()
        widgetScalingBtnsLayout.addWidget(self.inputField)
        widgetScalingBtnsLayout.addWidget(centralScrollArea)
        widgetScalingBtnsLayout.addWidget(self.scaleUpButton)
        widgetScalingBtnsLayout.addWidget(self.scaleDownButton)

        widgetScalingBtns = qtw.QFrame()
        widgetScalingBtns.setLayout(widgetScalingBtnsLayout)


        self.setCentralWidget(widgetScalingBtns)

        self.app = app
        self.uiScaler = GUIScalingManager()

        self.uiScaler.applyScaledStyle(self.app)
        self.uiScaler.applyScale(self.app)

        self.configure()

    def configure(self):
        self.uiScaler.scaleChanged.connect(self.handleScaleChanged)
        self.scaleUpButton.clicked.connect(lambda: self.uiScaler.scaleUp(self.app))
        self.scaleDownButton.clicked.connect(lambda: self.uiScaler.scaleDown(self.app))

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

    @staticmethod
    def widgetGroup() -> qtw.QWidget:

        inputField = qtw.QLineEdit("Hello World")
        inputLabel = qtw.QLabel("Sample Label")

        btnIcon = qta.icon("msc.home", color="#ff00ff")
        button = qtw.QPushButton("Sample Button")
        button.setIcon(btnIcon)

        treeWidget = qtw.QTreeWidget()
        MainWindow.populateTree(treeWidget)

        styledButton = qtw.QPushButton("Sample Styled Button")
        styledButton.setStyleSheet(f"""
            QPushButton{{ 
                background: orange;
                color: white;
                border: 1px solid black;
                padding: 20px;
            }}
        """)


        toolbar = qtw.QToolBar()
        helpAction = qtg.QAction(toolbar)
        helpIcon = qta.icon("msc.question", color="#ff0000")
        helpAction.setIcon(helpIcon)
        helpAction.setToolTip("Help Me")

        
        toolbar.addSeparator()
        toolbar.addAction(helpAction)
        toolbar.addSeparator()

        tableModel = TableModel()
        tableView = qtw.QTableView()
        tableView.setModel(tableModel)


        group = qtw.QGroupBox("Widget Group")
        layout = qtw.QVBoxLayout()

        layout.addWidget(inputLabel)
        layout.addWidget(inputField)
        layout.addWidget(treeWidget)
        layout.addWidget(tableView)
        layout.addWidget(button)
        layout.addWidget(styledButton)
        layout.addWidget(toolbar)

        group.setLayout(layout)
        return group

    @staticmethod
    def createGroupWidgets(count: int = 1) -> list[qtw.QGroupBox]:
        return [MainWindow.widgetGroup() for _ in range(count)]

if __name__ == "__main__":
    qApp = qtw.QApplication(sys.argv)
    qApp.setStyle("Fusion")

    window = MainWindow(qApp)
    window.show()

    sys.exit(qApp.exec())