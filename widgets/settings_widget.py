from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider
from PyQt5.QtCore import Qt


class SettingsWidget(QWidget):
    """
    Left settings panel; for now just shows 'alpha' slider etc.
    Controllers will later bind real logic.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 24, 0, 0)
        layout.setSpacing(12)

        self.alpha_label = QLabel("alpha")
        self.alpha_label.setAlignment(Qt.AlignLeft)

        self.alpha_slider = QSlider(Qt.Horizontal)
        self.alpha_slider.setRange(0, 100)
        self.alpha_slider.setValue(50)

        layout.addWidget(self.alpha_label)
        layout.addWidget(self.alpha_slider)
        layout.addStretch(1)
