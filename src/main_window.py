from PySide6.QtWidgets import QMainWindow, QTabWidget
from reticle.reticle import Reticle
from reticle.reticle_control_panel import ReticleControlPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        title = "ScopeAssist"

        self.setWindowTitle(title)
        self.resize(480, 270)

        self.tabs = QTabWidget()

        # --- Reticle Tab ---
        self.reticle_tab = ReticleControlPanel(Reticle())
        self.tabs.addTab(self.reticle_tab, "Reticle Controls")

        self.setCentralWidget(self.tabs)
