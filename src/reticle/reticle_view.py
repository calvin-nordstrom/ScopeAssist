import ctypes
from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QBrush
from PySide6.QtCore import Qt


user32 = ctypes.WinDLL("user32", use_last_error=True)

WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20


class ReticleView(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model
        self.model.changed.connect(self.update_view)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.hwnd = int(self.winId())
        self.make_click_through()

        self.app = QApplication.instance()
        self.update_view()

    def make_click_through(self):
        hwnd = self.hwnd

        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT

        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.model.color))
        painter.setPen(QPen(self.model.color))

        size = self.width()
        painter.drawEllipse(0, 0, size, size)

    def update_view(self):
        screens = self.app.screens()

        monitor = max(0, min(self.model.monitor, len(screens) - 1))
        screen = screens[monitor]
        geo = screen.geometry()

        size = self.model.radius * 2

        x = geo.x() + (geo.width() // 2) - (size // 2)
        y = geo.y() + (geo.height() // 2) - (size // 2)

        self.setGeometry(x, y, size, size)
        self.setWindowOpacity(self.model.transparency)

        if self.model.visible:
            self.show()
        else:
            self.hide()

        self.update()
