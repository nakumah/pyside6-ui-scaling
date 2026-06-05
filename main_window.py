import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc

import qtawesome as qta
import components as cpt
import utils.hotkeys as hotkeys
import resources.styling as sty


from table import TableModel
from utils.scaling import GUI_SCALER
from resources.colors import AppColors

class MainWindow(qtw.QMainWindow):
    def __init__(self, app: qtw.QApplication) -> None:
        super().__init__()

        self.fileMenu = qtw.QMenu("File")
        self.settingsAction: qtg.QAction = self.fileMenu.addAction(
            qta.icon("msc.gear", color="#00ff00"),
            "Settings",
        )
        self.customMenuBar = cpt.CustomMenuBar(self)
        self.customMenuBar.addMenu(self.fileMenu)
        self.setMenuBar(self.customMenuBar)

        self.inputField = cpt.VLineEdit("Hello World")
        self.scaleUpButton = cpt.VPushButton("Scale Up")
        self.scaleDownButton = cpt.VPushButton("Scale Down")
        self.customButton = cpt.VPushButton("My Button")

        scrollAreaLayout = qtw.QVBoxLayout()
        groupWidgetCount = 1
        groupWidgets = MainWindow.createGroupWidgets(groupWidgetCount)
        totalWidgetCount = 0
        for w in groupWidgets:
            c = w.layout().count()
            scrollAreaLayout.addWidget(w)
            totalWidgetCount += c

        self.setWindowTitle(f"Total Widgets \u003e {totalWidgetCount}")

        scrollAreaWidget = qtw.QWidget()
        scrollAreaWidget.setLayout(scrollAreaLayout)

        centralScrollArea = qtw.QScrollArea()
        centralScrollArea.setWidgetResizable(True)
        centralScrollArea.setWidget(scrollAreaWidget)

        contentLayout = qtw.QVBoxLayout()
        contentLayout.addWidget(self.inputField)
        contentLayout.addWidget(self.customButton)
        contentLayout.addWidget(centralScrollArea)
        contentLayout.addWidget(self.scaleUpButton)
        contentLayout.addWidget(self.scaleDownButton)
        contentLayout.setStretch(contentLayout.count() - 3, 1)

        widgetScalingBtns = qtw.QFrame()
        widgetScalingBtns.setLayout(contentLayout)

        self.setCentralWidget(widgetScalingBtns)

        self.app = app

        self.hotKeyManager = hotkeys.HotKeyManager(parent=self)

        self.configure()

        # trigger the scale
        GUI_SCALER.scaleTo(1.0)

        # apply the main stylesheet
        sty.setStyleSheet(self, "main_window")

    def configure(self):
        GUI_SCALER.scaleChanged.connect(self.handleScaleChanged)
        self.hotKeyManager.triggered.connect(self.handleHotKeyTriggered)

        self.scaleUpButton.clicked.connect(GUI_SCALER.scaleUp)
        self.scaleDownButton.clicked.connect(GUI_SCALER.scaleDown)

    def handleScaleChanged(self, scale: float) -> None:
        self.inputField.setText(f"Scale: {scale}")

    def handleHotKeyTriggered(self, key: object):
        if key == hotkeys.ZoomDirection.ZoomIn:
            GUI_SCALER.scaleUp()
        elif key == hotkeys.ZoomDirection.ZoomOut:
            GUI_SCALER.scaleDown()
        elif key == hotkeys.ZoomDirection.ZoomDefault:
            GUI_SCALER.resetScale()
        elif key == "quit":
            self.close()
        else:
            pass

    @staticmethod
    def populateTree(tree: qtw.QTreeWidget):
        count = 10

        for i in range(count):
            icon = qta.icon("msc.home", color="#ff11ee")
            treeItem = qtw.QTreeWidgetItem(tree)
            treeItem.setIcon(0, icon)
            treeItem.setText(0, f"Icon: {i + 1}")
            if i == 4:
                for j in range(count):
                    subItem = qtw.QTreeWidgetItem(treeItem)
                    icon2 = qta.icon("msc.home", color="#fa11ee")
                    subItem.setIcon(0, icon2)
                    subItem.setText(0, f"Icon {i}-{j + 1}")

    @staticmethod
    def buttonsGrid() -> qtw.QWidget:

        variantValues = ["danger", "dark", "primary", "success", "warning", "light"]

        layout = qtw.QHBoxLayout()

        for v in variantValues:
            btn = cpt.VPushButton(f"{v} button")
            btn.setProperty("buttonType", v)
            layout.addWidget(btn)

        layout.addWidget(cpt.VPushButton("default button"))

        widget = qtw.QFrame()
        widget.setLayout(layout)
        return widget

    @staticmethod
    def splitter() -> qtw.QSplitter:
        splitter = qtw.QSplitter()

        btn1 = cpt.VPushButton("Left Button")
        btn2 = cpt.VPushButton("Right Button")

        splitter.addWidget(btn1)
        splitter.addWidget(btn2)

        return splitter

    @staticmethod
    def sliders() -> qtw.QFrame:
        # vSlider = cpt.VSlider(qtc.Qt.Orientation.Vertical)
        hSlider = cpt.VSlider(qtc.Qt.Orientation.Horizontal)

        layout = qtw.QHBoxLayout()
        # layout.addWidget(vSlider)
        layout.addWidget(hSlider)
        
        frame = qtw.QFrame()
        frame.setFrameShape(qtw.QFrame.Shape.Box)
        frame.setLayout(layout)
        

        return frame

    @staticmethod
    def progressBars() -> qtw.QFrame:

        bar1 = cpt.VProgressBar()
        bar1.setProperty("class", "thin")
        bar1.setTextVisible(False)
        bar1.setRange(0, 0)

        bar2 = cpt.VProgressBar()
        bar2.setProperty("class", "thick")
        bar2.setRange(0, 10)
        bar2.setValue(7)

        bar3 = cpt.VProgressBar()
        bar3.setRange(0, 10)
        bar3.setValue(4)

        layout = qtw.QVBoxLayout()
        layout.addWidget(bar1)
        layout.addWidget(bar2)
        layout.addWidget(bar3)

        frame = qtw.QFrame()
        frame.setFrameShape(qtw.QFrame.Shape.Box)
        frame.setLayout(layout)

        return frame

    @staticmethod
    def comboBox() -> qtw.QComboBox:

        comboBox = cpt.VComboBox()

        for i in range(5):
            text = f"Item {i + 1}"
            if i % 2 == 0:
                pix = qtg.QPixmap(16, 16)
                pix.fill("orange")

                icon = qtg.QIcon(pix)
            else:
                icon = qta.icon("msc.home", color="#0001ff")

            comboBox.addItem(icon, text)

        return comboBox
    
    @staticmethod
    def tabWidget() -> qtw.QTabBar:

        tabs = cpt.VTabWidget()
        for i in range(5):
            text = f"Entry {i + 1}"        
            widget = cpt.VLabel(text)
            tabs.addTab(widget, text)
        
        tabs.setMovable(False)
        tabs.setTabsClosable(True)
        # tabs.setTabPosition(qtw.QTabWidget.TabPosition.West)
        return tabs
    
    @staticmethod
    def toolBtnToolBar() -> qtw.QToolBar:
        toolbar = cpt.VToolBar()

        for i in range(3):
            text = f"Btn {i + 1}"
            btn = qtw.QToolButton()
            btn.setText(text)
            icon = qta.icon("msc.home", color=AppColors.medium, color_active=AppColors.primary, color_hover=AppColors.primary)
            btn.setIcon(icon)
            btn.setToolButtonStyle(qtg.Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
            toolbar.addWidget(btn)

        toolbar.addSeparator()
        
        spacer = qtw.QWidget()
        spacer.setSizePolicy(
            qtw.QSizePolicy.Policy.Expanding,
            qtw.QSizePolicy.Policy.Preferred,
        )
        toolbar.addWidget(spacer)
        
        toolbar.addSeparator()

        btnEnd = qtw.QToolButton()
        btnEnd.setText("Btn End")
        toolbar.addWidget(btnEnd)

        return toolbar

    @staticmethod
    def widgetGroup(groupIndex: int = -1) -> qtw.QWidget:

        tabWidget = MainWindow.tabWidget()
        tabWidget.setMinimumHeight(300)

        lineEdit = cpt.VLineEdit("Custom Line Edit Hello World")
        textEdit = cpt.VTextEdit("Custom Text Edit Hello World")

        defaultLabel = cpt.VLabel("Default Label")

        dangerBoldLabel = cpt.VLabel("dangerBoldLabel")
        dangerBoldLabel.setProperty("fontWeight", "bold")
        dangerBoldLabel.setProperty("textColor", "danger")

        warningLightLabel = cpt.VLabel("warningLightLabel")
        warningLightLabel.setProperty("fontWeight", "light")
        warningLightLabel.setProperty("textColor", "warning")

        checkbox = cpt.VCheckBox("Sample Check box")
        comboBox = MainWindow.comboBox()

        btnIcon = qta.icon("msc.home", color="#ff00ff")
        button = cpt.VPushButton("Sample Button")
        button.setIcon(btnIcon)

        treeWidget = cpt.VTreeWidget()
        treeWidget.setMinimumHeight(200)
        MainWindow.populateTree(treeWidget)

        defaultButton = cpt.VPushButton("Default Button With Icon")
        defaultButton.setIcon(qta.icon("msc.home", color="#ff1ef2"))

        buttonsGrid = MainWindow.buttonsGrid()
        splitter = MainWindow.splitter()
        progressBars = MainWindow.progressBars()
        sliders = MainWindow.sliders()

        toolbar = qtw.QToolBar()
        helpAction = qtg.QAction(toolbar)
        helpIcon = qta.icon("msc.question", color="#ff0000")
        helpAction.setIcon(helpIcon)
        helpAction.setToolTip("Help Me")

        toolbar.addSeparator()
        toolbar.addAction(helpAction)
        toolbar.addSeparator()

        tableModel = TableModel()
        tableView = cpt.VTableView()
        tableView.setModel(tableModel)
        tableView.setMinimumHeight(200)

        toolButtonToolBar = MainWindow.toolBtnToolBar()

        groupIndexString = f" - {groupIndex}" if groupIndex > 0 else ""
        group = qtw.QGroupBox("Widget Group" + groupIndexString)
        layout = qtw.QVBoxLayout()

        layout.addWidget(toolButtonToolBar)
        layout.addWidget(tabWidget)
        layout.addWidget(splitter)
        layout.addWidget(progressBars)
        layout.addWidget(sliders)
        layout.addWidget(comboBox)
        layout.addWidget(defaultLabel)
        layout.addWidget(dangerBoldLabel)
        layout.addWidget(warningLightLabel)
        layout.addWidget(checkbox)
        layout.addWidget(lineEdit)
        layout.addWidget(textEdit)
        layout.addWidget(treeWidget)
        layout.addWidget(tableView)
        layout.addWidget(button)
        layout.addWidget(defaultButton)
        layout.addWidget(buttonsGrid)
        layout.addWidget(toolbar)
        layout.addStretch()

        group.setLayout(layout)
        return group

    @staticmethod
    def createGroupWidgets(count: int = 1) -> list[qtw.QGroupBox]:
        if count == 0:
            return []
        return [MainWindow.widgetGroup(i + 1) for i in range(count)]
