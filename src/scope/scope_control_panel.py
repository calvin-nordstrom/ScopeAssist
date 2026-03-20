from PySide6.QtWidgets import (
    QWidget, QLabel, QSlider, QPushButton, QVBoxLayout, QComboBox,
    QColorDialog, QApplication
)
from PySide6.QtCore import Qt
from scope.scope import Scope


class ScopeControlPanel(QWidget):
    def __init__(self, scope: Scope):
        super().__init__()

        self.scope = scope

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
        self.mag_slider.setRange(1, 10)
        self.mag_slider.setValue(self.scope.mag)
        self.mag_slider.valueChanged.connect(self.change_mag)

        layout.addWidget(self.mag_label)
        layout.addWidget(self.mag_slider)

        # --- Toggle ---
        self.toggle_button = QPushButton()
        self.toggle_button.clicked.connect(self.toggle_scope)
        layout.addWidget(self.toggle_button)

        self.scope.changed.connect(self._update_toggle_button)
        self._update_toggle_button()

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

    def toggle_scope(self):
        self.scope.toggle_visibility()

    def _update_toggle_button(self):
        if self.scope.visible:
            self.toggle_button.setText("Hide Scope")
        else:
            self.toggle_button.setText("Show Scope")
