from PySide6.QtCore import QObject, Signal, QSettings


class Scope(QObject):
    changed = Signal()

    def __init__(
        self,
        monitor=0,
        radius=300,
        mag=3.0,
        visible=False,
        activation_type="hold",
        activation_input="RIGHT"
    ):
        super().__init__()

        self._monitor = monitor
        self._radius = radius
        self._mag = mag
        self._visible = visible
        self._activation_type = activation_type
        self._activation_input = activation_input

    def to_dict(self):
        return {
            "monitor": self._monitor,
            "radius": self._radius,
            "mag": self._mag,
            "visible": self._visible,
            "activation_type": self._activation_type,
            "activation_input": self._activation_input,
        }

    def from_dict(self, data):
        self._monitor = data.get("monitor", 0)
        self._radius = data.get("radius", 300)
        self._mag = data.get("mag", 3.0)
        self._visible = data.get("visible", False)
        self._activation_type = data.get("activation_type", "toggle")
        self._activation_input = data.get("activation_input", "F6")

        self.changed.emit()

    def save(self):
        s = QSettings("ScopeAssist", "Scope")
        for k, v in self.to_dict().items():
            s.setValue(k, v)

    def load(self):
        s = QSettings("ScopeAssist", "Scope")
        self.from_dict({
            "monitor": int(s.value("monitor", 0)),
            "radius": int(s.value("radius", 300)),
            "mag": float(s.value("mag", 3.0)),
            "visible": s.value("visible", False) in [True, "true", "1"],
            "activation_type": s.value("activation_type", "toggle"),
            "activation_input": s.value("activation_input", "F6"),
        })

    @property
    def monitor(self):
        return self._monitor

    @property
    def radius(self):
        return self._radius
    
    @property
    def mag(self):
        return self._mag

    @property
    def visible(self):
        return self._visible
    
    @property
    def activation_type(self):
        return self._activation_type

    @property
    def activation_input(self):
        return self._activation_input

    def set_monitor(self, monitor):
        if self._monitor != monitor:
            self._monitor = monitor
            self.changed.emit()

    def set_radius(self, radius):
        radius = max(1, radius)
        if self._radius != radius:
            self._radius = radius
            self.changed.emit()
    
    def set_mag(self, mag):
        mag = max(1.0, min(10.0, mag))
        if self._mag != mag:
            self._mag = mag
            self.changed.emit()

    def set_visible(self, visible):
        if self._visible != visible:
            self._visible = visible
            self.changed.emit()

    def toggle_visibility(self):
        self.set_visible(not self._visible)

    def set_activation_type(self, t):
        if t != self._activation_type:
            self._activation_type = t
            self.changed.emit()

    def set_activation_input(self, i):
        if i != self._activation_input:
            self._activation_input = i
            self.changed.emit()
