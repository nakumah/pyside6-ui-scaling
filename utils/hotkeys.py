from enum import IntEnum

import PySide6.QtWidgets as qtw
import PySide6.QtGui as qtg
import PySide6.QtCore as qtc


class ZoomDirection:
    ZoomDefault = 0
    ZoomIn = 1
    ZoomOut = 2

class VShortcut(qtg.QShortcut):
    cmdTriggered = qtc.Signal(object)

    def __init__(self, cmdKey: str | int, sequence: qtg.QKeySequence, parent: qtc.QObject):
        super().__init__(sequence, parent)

        self.__cmdKey: str | int = cmdKey

        self.__configure()

    def __configure(self):
        self.activated.connect(self.__handleActivated)
        self.activatedAmbiguously.connect(self.__handleAmbiguousConnection)

    def __handleAmbiguousConnection(self):
        pass

    def __handleActivated(self):
        self.cmdTriggered.emit(self.__cmdKey)

    def cmdKey(self):
        return self.__cmdKey

    def setCmdKey(self, cmdKey: str):
        self.__cmdKey = cmdKey


class HotKeyManager(qtc.QObject):
    triggered = qtc.Signal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._hotKeys: dict[int | str,  VShortcut] = {
            ZoomDirection.ZoomIn: VShortcut(ZoomDirection.ZoomIn, qtg.QKeySequence("Ctrl+Up"), kwargs.get("parent", None)),
            ZoomDirection.ZoomOut: VShortcut(ZoomDirection.ZoomOut, qtg.QKeySequence("Ctrl+Down"), kwargs.get("parent", None)),
            ZoomDirection.ZoomDefault: VShortcut(ZoomDirection.ZoomDefault, qtg.QKeySequence("Ctrl+0"), kwargs.get("parent", None)),
            "quit": VShortcut("quit", qtg.QKeySequence("Ctrl+Q"), kwargs.get("parent", None))
        }

        self._configure()

    def _configure(self):
        for shorcut in self._hotKeys.values():
            shorcut.cmdTriggered.connect(self._handleShortcutTriggered)

    def _handleShortcutTriggered(self, value: object):
        self.triggered.emit(value)