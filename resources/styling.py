import os
import inspect
import re

from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QWidget

from resources.colors import AppColors


def qrc_style_str(filename: str):
    """
    returns the file name of the qrc file
    :param filename:
    :return:
    """
    return f":/qss/{filename}"


def changeWidgetBackground(widget: QWidget, color: str):
    """
    Sets the background of the widget to color
    :param widget:
    :param color:
    :return:
    """
    widget.setAutoFillBackground(True)
    palette = widget.palette()
    palette.setColor(QPalette.ColorRole.Window, QColor(color))
    widget.setPalette(palette)


def __applyTheme(qss: str, colorClass) -> str:
    """
    Replace @variable_name tokens in a QSS string with values from a color class.

    Args:
        qss: QSS stylesheet string with @variable_name tokens
        colorClass: A class (or instance) whose attributes define the token values

    Returns:
        QSS string with all tokens replaced by their corresponding values
    """
    # Extract all class-level attributes (skip dunders and callables)
    if isinstance(colorClass, type):
        members = {
            k: v
            for k, v in vars(colorClass).items()
            if not k.startswith("_") and not callable(v)
        }
    else:
        members = {
            k: v
            for k, v in inspect.getmembers(colorClass)
            if not k.startswith("_") and not callable(v)
        }

    def replacer(match):
        token = match.group(1)  # variable name without @
        if token in members:
            return members[token]
        return match.group(0)  # leave unknown tokens untouched

    # Build pattern matching @word_with_underscores
    pattern = re.compile(r"@([a-zA-Z_][a-zA-Z0-9_]*)")
    return pattern.sub(replacer, qss) + "\n"


def parseStyleSheet(qss: str):
    """
    Replace all variable placeholders with their respective values
    """
    return __applyTheme(qss, AppColors)


def readStyle(filename: str):
    """
    reads data from a file.
    pass the file name without the extension (.qss)
    @param filename:
    @return:
    """
    try:
        f = QFile(f"{qrc_style_str(filename)}.qss")
        f.open(QFile.OpenModeFlag.ReadOnly)
        data: str = f.readAll().data().decode("utf-8")
        f.close()
        return parseStyleSheet(data)
    except OSError as e:
        print("Reading file error", e)


def readStyles(filenames: list[str]):
    """
    reads data from multiples, combines and returns as a single str
    @param filenames:
    @return:
    """
    style = ""
    for file in filenames:
        style += readStyle(file)
    return style


def loadApplicationQSS() -> str:
    qssFolder = Path("E:/ComplexFluids/PlayGround/ui-scaling/resources/qss")
    qssFiles = [file.stem for file in qssFolder.iterdir() if file.is_file()]
    qss = readStyles(qssFiles)
    return qss


def loadApplicationBaseQSS() -> str:
    styles = [
        "q_menu", 
        "q_scrollbar",
        "q_splitter",
    ]
    return readStyles(styles)


def setStyleSheet(widget: QWidget, name: str, extra: str = ""):

    if name == "main_window":
        qss = loadApplicationBaseQSS()
    else:
        qss = readStyle(name) + extra
    widget.setStyleSheet(qss)
