from PyQt5.QtWidgets import QPushButton

class HoverButton(QPushButton):
    def __init__(self, text, parent=None, default_style="", hover_style="", disabled_style=""):
        super().__init__(text, parent)
        self.default_style = default_style
        self.hover_style = hover_style
        self.disabled_style = disabled_style
        self.setStyleSheet(self.default_style)
    
    def enterEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(self.hover_style)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(self.default_style)
        super().leaveEvent(event)
    
    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        if enabled:
            self.setStyleSheet(self.default_style)
        else:
            self.setStyleSheet(self.disabled_style)
