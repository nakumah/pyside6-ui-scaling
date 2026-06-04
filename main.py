import os
import sys
import PySide6.QtWidgets as qtw

from utils.scaling import GUI_SCALER
from main_window import MainWindow


os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support
from resources import resource_rc # type: ignore


if __name__ == "__main__":
    qApp = qtw.QApplication(sys.argv)
    qApp.setStyle("Fusion")

    GUI_SCALER.setQApplicationInstance(qApp)

    window = MainWindow(qApp)
    window.show()

    sys.exit(qApp.exec())