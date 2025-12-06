from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Settings Window</b>"))
        layout.addWidget(QLabel("alpha"))
        layout.addStretch()
