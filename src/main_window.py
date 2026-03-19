from PySide6.QtWidgets import QMainWindow, QTabWidget
from reticle.reticle import Reticle
from reticle.reticle_view import ReticleView
from reticle.reticle_control_panel import ReticleControlPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ScopeAssist")
        self.resize(480, 270)

        self.tabs = QTabWidget()

        self.reticle = Reticle()
        self.reticle.load()
        self.reticle_view = ReticleView(self.reticle)
        self.reticle_tab = ReticleControlPanel(self.reticle)
        self.tabs.addTab(self.reticle_tab, "Reticle Controls")

        self.setCentralWidget(self.tabs)

    def closeEvent(self, event):
        self.reticle.save()
        
        super().closeEvent(event)
