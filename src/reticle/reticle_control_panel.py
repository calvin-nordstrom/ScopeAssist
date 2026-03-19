from PySide6.QtWidgets import (
    QWidget, QLabel, QSlider, QPushButton, QVBoxLayout, QComboBox,
    QColorDialog, QApplication
)
from PySide6.QtCore import Qt


class ReticleControlPanel(QWidget):
    def __init__(self, model):
        super().__init__()

        self.model = model

        layout = QVBoxLayout()

        # --- Monitor ---
        layout.addWidget(QLabel("Monitor"))
        self.screen_dropdown = QComboBox()

        screens = QApplication.instance().screens()
        for i in range(len(screens)):
            self.screen_dropdown.addItem(f"Monitor {i}")

        self.screen_dropdown.currentIndexChanged.connect(self.change_monitor)
        layout.addWidget(self.screen_dropdown)

        # --- Radius ---
        self.radius_label = QLabel(f"Radius: {self.model.radius}")
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(1, 10)
        self.radius_slider.setValue(self.model.radius)
        self.radius_slider.valueChanged.connect(self.change_radius)

        layout.addWidget(self.radius_label)
        layout.addWidget(self.radius_slider)

        # --- Transparency ---
        self.transparency_label = QLabel(
            f"Transparency: {self.model.transparency:.2f}"
        )
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(int(self.model.transparency * 100))
        self.transparency_slider.valueChanged.connect(self.change_transparency)

        layout.addWidget(self.transparency_label)
        layout.addWidget(self.transparency_slider)

        # --- Color ---
        self.color_button = QPushButton("Change Color")
        self.color_button.clicked.connect(self.pick_color)
        layout.addWidget(self.color_button)

        # --- Show / Hide ---
        self.toggle_button = QPushButton()
        self.toggle_button.clicked.connect(self.toggle_reticle)

        layout.addWidget(self.toggle_button)

        self.model.changed.connect(self._update_toggle_button_text)
        self._update_toggle_button_text()

        layout.addStretch()
        self.setLayout(layout)

    # --- Handlers ---
    def change_monitor(self, monitor):
        self.model.set_monitor(monitor)

    def change_radius(self, radius):
        self.radius_label.setText(f"Radius: {radius}")
        self.model.set_radius(radius)

    def change_transparency(self, transparency):
        alpha = transparency / 100
        self.transparency_label.setText(f"Transparency: {alpha:.2f}")
        self.model.set_transparency(alpha)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.model.set_color(color.name())

    def toggle_reticle(self):
        self.model.toggle_visibility()

    def _update_toggle_button_text(self):
        if self.model.visible:
            self.toggle_button.setText("Hide Reticle")
        else:
            self.toggle_button.setText("Show Reticle")
