from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Settings Window"))
        layout.addWidget(QLabel("alpha"))
        layout.addStretch(1)

        self.setLayout(layout)
