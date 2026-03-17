from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt


class Reticle(QWidget):
    def __init__(self, monitor=0, radius=2, transparency=0.8, color="white"):
        super().__init__()

        self.monitor = monitor
        self.radius = radius
        self.transparency = transparency
        self.color = QColor(color)

        # Window setup
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setWindowOpacity(self.transparency)

        # Monitor setup
        self.app = QApplication.instance()
        screens = self.app.screens()

        if monitor >= len(screens):
            monitor = 0

        self.target_screen = screens[monitor]
        self._update_geometry()

        self.show()

    # --- Drawing ---
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(self.color))
        painter.setPen(QPen(self.color))

        size = self.width()
        painter.drawEllipse(0, 0, size, size)

    # --- Layout ---
    def _update_geometry(self):
        screen_geometry = self.target_screen.geometry()

        size = self.radius * 2
        x = screen_geometry.x() + (screen_geometry.width() // 2) - (size // 2)
        y = screen_geometry.y() + (screen_geometry.height() // 2) - (size // 2)

        self.setGeometry(x, y, size, size)

    # --- Updates ---
    def update_reticle(self, monitor=None, radius=None, transparency=None,
                       color=None):
        screens = self.app.screens()

        if monitor is not None:
            monitor = max(0, min(monitor, len(screens) - 1))
            self.monitor = monitor
            self.target_screen = screens[monitor]

            geo = self.target_screen.geometry()
            self.move(geo.x(), geo.y())

        if radius is not None:
            self.radius = max(1, radius)

        if transparency is not None:
            self.transparency = transparency
            self.setWindowOpacity(self.transparency)

        if color is not None:
            self.color = QColor(color)

        self._update_geometry()
        self.update()

    # --- Visibility controls ---
    def show_reticle(self):
        self.show()

    def hide_reticle(self):
        self.hide()
