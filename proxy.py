from typing import Optional, cast
from PySide6.QtWidgets import QTabWidget, QWidget, QProxyStyle, QStyle, QStyleOptionTab, QStyleOption
from PySide6.QtCore import QSize
from PySide6.QtGui import QPainter

class HorizontalTextTabStyle(QProxyStyle):
    def sizeFromContents(
        self, 
        content_type: QStyle.ContentsType, 
        option: QStyleOption, 
        size: QSize, 
        widget: Optional[QWidget] = None
    ) -> QSize:
        # Get base size calculation
        current_size: QSize = super().sizeFromContents(content_type, option, size, widget)
        
        # Verify widget and parent existence safely before inspecting tab position
        if (content_type == QStyle.ContentsType.CT_TabBarTab 
                and widget is not None 
                and widget.parentWidget() is not None):
            
            parent: QWidget = widget.parentWidget()
            # Ensure the parent is a QTabWidget before checking tabPosition
            if isinstance(parent, QTabWidget) and parent.tabPosition() in (QTabWidget.TabPosition.West, QTabWidget.TabPosition.East):
                return QSize(current_size.height(), current_size.width())
                
        return current_size

    def drawControl(
        self, 
        element: QStyle.ControlElement, 
        option: QStyleOption, 
        painter: QPainter, 
        widget: Optional[QWidget] = None
    ) -> None:
        # Intercept vertical tab labels to render them horizontally
        if (element == QStyle.ControlElement.CE_TabBarTabLabel 
                and widget is not None 
                and widget.parentWidget() is not None):
            
            parent: QWidget = widget.parentWidget()
            if isinstance(parent, QTabWidget) and parent.tabPosition() in (QTabWidget.TabPosition.West, QTabWidget.TabPosition.East):
                if isinstance(option, QStyleOptionTab):
                    # Cast to concrete class to satisfy strict type-checkers for custom property modifications
                    tab_option: QStyleOptionTab = cast(QStyleOptionTab, option)
                    tab_option.shape = QTabWidget.TabShape.RoundedNorth
                    
        super().drawControl(element, option, painter, widget)
