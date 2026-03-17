from PySide6.QtWidgets import (
    QWidget, QLabel, QSlider, QPushButton, QVBoxLayout, QComboBox,
    QColorDialog
)
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication


class ReticleControlPanel(QWidget):
    def __init__(self, reticle):
        super().__init__()

        self.reticle = reticle

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
        self.radius_label = QLabel(f"Radius: {self.reticle.radius}")
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(1, 10)
        self.radius_slider.setValue(self.reticle.radius)
        self.radius_slider.valueChanged.connect(self.change_radius)

        layout.addWidget(self.radius_label)
        layout.addWidget(self.radius_slider)

        # --- Transparency ---
        self.transparency_label = QLabel(f"Transparency: {self.reticle.transparency:.2f}")
        self.transparency_slider = QSlider(Qt.Horizontal)
        self.transparency_slider.setRange(0, 100)
        self.transparency_slider.setValue(int(self.reticle.transparency * 100))
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

        self._update_toggle_button_text()

        layout.addStretch()

        self.setLayout(layout)

    # --- Handlers ---

    def change_monitor(self, monitor):
        self.reticle.update_reticle(monitor=monitor)

    def change_radius(self, radius):
        self.radius_label.setText(f"Radius: {radius}")
        self.reticle.update_reticle(radius=radius)

    def change_transparency(self, transparency):
        alpha = transparency / 100
        self.transparency_label.setText(f"Transparency: {alpha:.2f}")
        self.reticle.update_reticle(transparency=alpha)

    def pick_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.reticle.update_reticle(color=color.name())

    def toggle_reticle(self):
        if self.reticle.isVisible():
            self.reticle.hide_reticle()
        else:
            self.reticle.show_reticle()

        self._update_toggle_button_text()


    def _update_toggle_button_text(self):
        if self.reticle.isVisible():
            self.toggle_button.setText("Hide Reticle")
        else:
            self.toggle_button.setText("Show Reticle")
