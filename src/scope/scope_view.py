import ctypes
from ctypes import wintypes
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QRegion
from PySide6.QtWidgets import QWidget, QApplication
from scope.scope import Scope


user32 = ctypes.WinDLL("user32", use_last_error=True)
mag = ctypes.WinDLL("Magnification.dll")

WS_CHILD = 0x40000000
WS_VISIBLE = 0x10000000
WS_EX_LAYERED = 0x00080000
WS_EX_TRANSPARENT = 0x00000020
GWL_EXSTYLE = -20


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]


class MAGTRANSFORM(ctypes.Structure):
    _fields_ = [("v", ctypes.c_float * 9)]


class ScopeView(QWidget):
    def __init__(self, scope: Scope):
        super().__init__()

        self.scope = scope
        self.scope.changed.connect(self.update_view)

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.app = QApplication.instance()

        self.hwnd = int(self.winId())
        self.make_click_through()

        if not mag.MagInitialize():
            raise RuntimeError("MagInitialize failed")

        self.mag_hwnd = None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_source)
        self.timer.start(16)

        self.update_view()

    def make_click_through(self):
        hwnd = self.hwnd

        style = user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        style |= WS_EX_LAYERED | WS_EX_TRANSPARENT

        user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

    def create_magnifier(self):
        if self.mag_hwnd:
            return

        self.mag_hwnd = user32.CreateWindowExW(
            0,
            "Magnifier",
            None,
            WS_CHILD | WS_VISIBLE,
            0, 0,
            self.width(),
            self.height(),
            self.hwnd,
            None,
            None,
            None
        )

        if not self.mag_hwnd:
            raise ctypes.WinError(ctypes.get_last_error())

    def set_transform(self):
        matrix = MAGTRANSFORM()
        for i in range(9):
            matrix.v[i] = 0.0

        matrix.v[0] = self.scope.mag
        matrix.v[4] = self.scope.mag
        matrix.v[8] = 1.0

        mag.MagSetWindowTransform(
            self.mag_hwnd,
            ctypes.byref(matrix)
        )

    def update_view(self):
        screens = self.app.screens()

        monitor = max(0, min(self.scope.monitor, len(screens) - 1))
        screen = screens[monitor]
        geo = screen.geometry()

        diameter = self.scope.radius * 2

        x = geo.x() + (geo.width() // 2) - (diameter // 2)
        y = geo.y() + (geo.height() // 2) - (diameter // 2)

        self.setGeometry(x, y, diameter, diameter)
        self.setMask(QRegion(0, 0, diameter, diameter, QRegion.Ellipse))

        self.create_magnifier()
        self.set_transform()

        if self.scope.visible:
            self.show()
        else:
            self.hide()

        self.update_source()

    def update_source(self):
        if not self.mag_hwnd or not self.scope.visible:
            return

        center = self.mapToGlobal(self.rect().center())

        x = center.x()
        y = center.y()

        size = int((self.scope.radius * 2) / self.scope.mag)

        rect = RECT(
            x - size // 2,
            y - size // 2,
            x + size // 2,
            y + size // 2
        )

        mag.MagSetWindowSource(self.mag_hwnd, rect)

    def resizeEvent(self, event):
        if self.mag_hwnd:
            user32.MoveWindow(
                self.mag_hwnd,
                0, 0,
                self.width(),
                self.height(),
                True
            )
        super().resizeEvent(event)

    def closeEvent(self, event):
        mag.MagUninitialize()
        super().closeEvent(event)
