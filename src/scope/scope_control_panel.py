from PySide6.QtWidgets import (
    QWidget, QLabel, QSlider, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox,
    QApplication, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QEvent
from scope.scope import Scope
from scope.scope_input_listener import ScopeInputListener


class ScopeControlPanel(QWidget):
    def __init__(self, scope: Scope):
        super().__init__()

        self.scope = scope
        self._capturing_input = False
        self.scope_input_listener = ScopeInputListener(self.scope)

        layout = QVBoxLayout()

        # --- Monitor ---
        layout.addWidget(QLabel("Monitor"))
        self.screen_dropdown = QComboBox()
        screens = QApplication.instance().screens()
        for i in range(len(screens)):
            self.screen_dropdown.addItem(f"Monitor {i}")
        self.screen_dropdown.currentIndexChanged.connect(self.change_monitor)
        self.screen_dropdown.setCurrentIndex(self.scope.monitor)
        layout.addWidget(self.screen_dropdown)

        # --- Radius ---
        self.radius_label = QLabel(f"Radius: {self.scope.radius}")
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(50, 500)
        self.radius_slider.setValue(self.scope.radius)
        self.radius_slider.valueChanged.connect(self.change_radius)
        layout.addWidget(self.radius_label)
        layout.addWidget(self.radius_slider)

        # --- Magnification ---
        self.mag_label = QLabel(f"Magnification: {self.scope.mag}x")
        self.mag_slider = QSlider(Qt.Horizontal)
        self.mag_slider.setRange(1.0, 10.0)
        self.mag_slider.setValue(self.scope.mag)
        self.mag_slider.valueChanged.connect(self.change_mag)
        layout.addWidget(self.mag_label)
        layout.addWidget(self.mag_slider)

        self.activation_layout = QHBoxLayout()

        # --- Activation Type ---
        self.activation_type_layout = QVBoxLayout()
        self.activation_type_layout.addWidget(QLabel("Activation Type"))
        self.activation_radio_layout = QHBoxLayout()
        self.hold_radio = QRadioButton("Hold")
        self.toggle_radio = QRadioButton("Toggle")
        self.activation_type_group = QButtonGroup(self)
        self.activation_type_group.addButton(self.hold_radio)
        self.activation_type_group.addButton(self.toggle_radio)
        self.activation_radio_layout.addWidget(self.hold_radio)
        self.activation_radio_layout.addWidget(self.toggle_radio)
        if self.scope.activation_type == "hold":
            self.hold_radio.setChecked(True)
        else:
            self.toggle_radio.setChecked(True)
        self.hold_radio.toggled.connect(self._on_activation_changed)
        self.toggle_radio.toggled.connect(self._on_activation_changed)
        self.activation_type_layout.addLayout(self.activation_radio_layout)
        self.activation_layout.addLayout(self.activation_type_layout)

        # --- Activation Input ---
        self.activation_input_layout = QVBoxLayout()
        self.activation_input_layout.addWidget(QLabel("Activation Input"))
        self.input_button = QPushButton(self.scope.activation_input)
        self.input_button.clicked.connect(self.capture_input)
        self.activation_input_layout.addWidget(self.input_button)
        self.activation_layout.addLayout(self.activation_input_layout)

        layout.addLayout(self.activation_layout)

        # --- Toggle ---
        self.toggle_button = QPushButton()
        self.toggle_button.clicked.connect(self.toggle_scope)
        layout.addWidget(self.toggle_button)

        self.scope.changed.connect(self._update_toggle_button)
        self.scope.changed.connect(self._update_activation_inputs)
        self._update_toggle_button()
        self._update_activation_inputs()

        layout.addStretch()
        self.setLayout(layout)

    # --- Handlers ---
    def change_monitor(self, monitor):
        self.scope.set_monitor(monitor)

    def change_radius(self, radius):
        self.radius_label.setText(f"Radius: {radius}")
        self.scope.set_radius(radius)

    def change_mag(self, mag):
        self.mag_label.setText(f"Magnification: {mag}x")
        self.scope.set_mag(mag)

    def _on_activation_changed(self):
        if self.hold_radio.isChecked():
            self.scope.set_activation_type("hold")
        else:
            self.scope.set_activation_type("toggle")

    def capture_input(self):
        self.input_button.setEnabled(False)
        self.input_button.setText("Press key or click...")
        self._capturing_input = True
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj, event):
        if not self._capturing_input:
            return super().eventFilter(obj, event)

        # --- Keyboard ---
        if event.type() == QEvent.KeyPress:
            key_name = self._qt_key_to_string(event.key())
            self._finish_input_capture(key_name)
            return True

        # --- Mouse ---
        elif event.type() == QEvent.MouseButtonPress:
            btn_name = self._qt_mouse_to_string(event.button())
            self._finish_input_capture(btn_name)
            return True

        return super().eventFilter(obj, event)

    def _finish_input_capture(self, name):
        try:
            self.scope.set_activation_input(name)
            self.input_button.setText(name)
        finally:
            self.input_button.setEnabled(True)
            self._capturing_input = False
            QApplication.instance().removeEventFilter(self)

    def _update_activation_inputs(self):
        self.hold_radio.blockSignals(True)
        self.toggle_radio.blockSignals(True)

        if self.scope.activation_type == "hold":
            self.hold_radio.setChecked(True)
        else:
            self.toggle_radio.setChecked(True)

        self.hold_radio.blockSignals(False)
        self.toggle_radio.blockSignals(False)

    def toggle_scope(self):
        self.scope.toggle_visibility()

    def _update_toggle_button(self):
        if self.scope.visible:
            self.toggle_button.setText("Hide Scope")
        else:
            self.toggle_button.setText("Show Scope")

    # --- Helpers ---
    def _qt_key_to_string(self, key):
        if Qt.Key_A <= key <= Qt.Key_Z:
            return chr(key)

        if Qt.Key_0 <= key <= Qt.Key_9:
            return chr(key)

        special = {
            Qt.Key_F1: "F1",
            Qt.Key_F2: "F2",
            Qt.Key_F3: "F3",
            Qt.Key_F4: "F4",
            Qt.Key_F5: "F5",
            Qt.Key_F6: "F6",
            Qt.Key_F7: "F7",
            Qt.Key_F8: "F8",
            Qt.Key_F9: "F9",
            Qt.Key_F10: "F10",
            Qt.Key_F11: "F11",
            Qt.Key_F12: "F12",
            Qt.Key_Shift: "SHIFT",
            Qt.Key_Control: "CTRL",
            Qt.Key_Alt: "ALT",
            Qt.Key_Space: "SPACE",
            Qt.Key_Escape: "ESC",
        }

        return special.get(key, str(key))

    def _qt_mouse_to_string(self, button):
        mapping = {
            Qt.LeftButton: "LEFT",
            Qt.RightButton: "RIGHT",
            Qt.MiddleButton: "MIDDLE",
        }
        return mapping.get(button, "UNKNOWN")
