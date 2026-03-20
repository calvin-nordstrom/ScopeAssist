from PySide6.QtCore import QObject, Signal, QSettings
from PySide6.QtGui import QColor


class Reticle(QObject):
    changed = Signal()

    def __init__(self, monitor=0, radius=2, transparency=0.8, color="white"):
        super().__init__()

        self._monitor = monitor
        self._radius = radius
        self._transparency = transparency
        self._color = QColor(color)
        self._visible = False

    def to_dict(self):
        return {
            "monitor": self._monitor,
            "radius": self._radius,
            "transparency": self._transparency,
            "color": self._color.name(),
            "visible": self._visible,
        }

    def from_dict(self, data):
        self._monitor = data.get("monitor", 0)
        self._radius = data.get("radius", 2)
        self._transparency = data.get("transparency", 0.8)
        self._color = QColor(data.get("color", "white"))
        self._visible = data.get("visible", False)

        self.changed.emit()

    def save(self):
        s = QSettings("ScopeAssist", "Reticle")
        for k, v in self.to_dict().items():
            s.setValue(k, v)

    def load(self):
        s = QSettings("ScopeAssist", "Reticle")
        self.from_dict({
            "monitor": int(s.value("monitor", 0)),
            "radius": int(s.value("radius", 2)),
            "transparency": float(s.value("transparency", 0.8)),
            "color": s.value("color", "white"),
            "visible": s.value("visible", False) in [True, "true", "1"],
        })

    @property
    def monitor(self):
        return self._monitor

    @property
    def radius(self):
        return self._radius

    @property
    def transparency(self):
        return self._transparency

    @property
    def color(self):
        return self._color

    @property
    def visible(self):
        return self._visible

    def set_monitor(self, monitor):
        if self._monitor != monitor:
            self._monitor = monitor
            self.changed.emit()

    def set_radius(self, radius):
        radius = max(1, radius)
        if self._radius != radius:
            self._radius = radius
            self.changed.emit()

    def set_transparency(self, transparency):
        transparency = max(0.0, min(1.0, transparency))
        if self._transparency != transparency:
            self._transparency = transparency
            self.changed.emit()

    def set_color(self, color):
        new_color = QColor(color)
        if self._color != new_color:
            self._color = new_color
            self.changed.emit()

    def set_visible(self, visible: bool):
        if self._visible != visible:
            self._visible = visible
            self.changed.emit()

    def toggle_visibility(self):
        self.set_visible(not self._visible)
