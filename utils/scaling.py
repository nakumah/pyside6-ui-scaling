import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc
import PySide6.QtGui as qtg


class ScaledStyle(qtw.QProxyStyle):
    def __init__(self, baseStyle: qtw.QStyle, scale: int = 1):
        super().__init__(baseStyle)
        self._scale: float = scale

    def setScale(self, scale: float):
        self._scale: float = scale

    def pixelMetric(self, metric, option=None, widget=None):
        value = super().pixelMetric(metric, option, widget)

        # clamp the scaling to be at least 1
        return int(value * self._scale) or 1


class GUIScalingManager(qtc.QObject):
    scaleChanged = qtc.Signal(float)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)


        self.__baseScale = 1.0
        self.__scale = 1.9
        self.__scaleLB = 0.7
        self.__scaleUB = 2.0
        self.__scaleStep = 0.2
        self.__defaultFontSize = 10.0

        self.__app: qtw.QApplication = None
        self.__scaledStyle: ScaledStyle = None

        # throttle the scaling to trigger every 30 Frames
        self.__scaleTimer = qtc.QTimer()
        self.__scaleTimer.setSingleShot(True)
        self.__scaleTimer.timeout.connect(self.__applyScale)
        self.__scaleTimerInterval = 32  # ~ 30 FPS
        self.__scaleTimer.setInterval(self.__scaleTimerInterval)


    # region override

    # endregion

    # region setters

    def setQApplicationInstance(self, qApp: qtw.QApplication) -> None:
        self.__app = qApp
        self.__scaledStyle = ScaledStyle(self.__app.style())
        self.__app.setStyle(self.__scaledStyle)

    def setScale(self, scale: float) -> None:
        self.__scale = self.__clampToScaleRange(scale)
        self.applyScale()

    # endregion
    
    # region getters
    def stepDownScale(self) -> float:
        return self.__clampToScaleRange(self.__scale - self.__scaleStep)

    def stepUpScale(self) -> float:
        return self.__clampToScaleRange(self.__scale + self.__scaleStep)

    def baseZoom(self) -> float:
        return self.__baseScale
    
    def currentFont(self) -> qtg.QFont:
        if self.__app is None:
            return qtg.QFont()
        return self.__app.font()
    
    def baseFontSize(self) -> float:
        return self.__defaultFontSize

    # endregion

    # region workers

    def __applyScale(self) -> None:
        if not isinstance(self.__app, qtw.QApplication):
            return

        self.__scaledStyle.setScale(self.__scale)

        font = qtg.QFont(self.__app.font())
        font.setPointSizeF(self.__defaultFontSize * self.__scale)
        self.__app.setFont(font)

        # flag the scale as changed
        self.scaleChanged.emit(self.__scale)

    def applyScale(self) -> None:
        if self.__scaleTimer.isActive():
            self.__scaleTimer.stop()
        self.__scaleTimer.start(self.__scaleTimerInterval)

    def __clampToScaleRange(self, s: float) -> float:
        return max(self.__scaleLB, min(s, self.__scaleUB))

    def scaleUp(self):
        s = self.stepUpScale()
        self.setScale(s)

    def scaleDown(self):
        s = self.stepDownScale()
        self.setScale(s)

    def resetScale(self):
        self.setScale(self.__baseScale)

    def scaleTo(self, targetScale: float):
        self.setScale(self.__clampToScaleRange(targetScale))

    # endregion

GUI_SCALER = GUIScalingManager()