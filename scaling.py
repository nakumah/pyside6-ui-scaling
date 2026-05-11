
import PySide6.QtWidgets as qtw
import PySide6.QtCore as qtc


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
        self.__scale = 1.0
        self.__scaleLB = 0.7
        self.__scaleUB = 2.0
        self.__scaleStep = 0.1

        self.__defaultFontSize = 13.0
        self.__scaledStyle = None

    def setScale(self, scale: float, app: qtw.QApplication) -> None:
        self.__scale = self.__clampToScaleRange(scale)
        self.applyScale(app)
        self.scaleChanged.emit(self.__scale)

    def applyScaledStyle(self, app: qtw.QApplication) -> qtw.QProxyStyle:
        self.__scaledStyle = ScaledStyle(app.style())
        app.setStyle(self.__scaledStyle)
        return self.__scaledStyle

    def applyScale(self, app: qtw.QApplication) -> None:

        self.__scaledStyle.setScale(self.__scale)

        # newFont = app.font()
        # newFont.setPointSizeF(self.__defaultFontSize * self.__scale)
        # app.setFont(newFont)

        app.setStyleSheet(
            f"""
                QWidget{{
                    font-size: {self.__defaultFontSize * self.__scale}px;
                }}
            """
        )

        # for widget in app.allWidgets():
        #     widget.updateGeometry()
        #     widget.update()

    def __clampToScaleRange(self, s: float) -> float:
        return max(self.__scaleLB, min(s, self.__scaleUB))

    def scaleUp(self, app: qtw.QApplication):
        s = self.__clampToScaleRange(self.__scale + self.__scaleStep)
        self.setScale(s, app)

    def scaleDown(self, app: qtw.QApplication):
        s = self.__clampToScaleRange(self.__scale - self.__scaleStep)
        self.setScale(s, app)

    def resetScale(self, app: qtw.QApplication):
        self.setScale(self.__baseScale, app)

    def scaleTo(self, targetScale: float, app: qtw.QApplication):
        self.setScale(self.__clampToScaleRange(targetScale), app)
