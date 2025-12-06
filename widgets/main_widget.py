from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Image")

        # --- Layout ---
        layout = QVBoxLayout()

        # Buttons and status
        self.load_button = QPushButton("Load Images")
        self.crop_button = QPushButton("Crop Images")
        self.status_label = QLabel("Ready.")

        layout.addWidget(self.load_button)
        layout.addWidget(self.crop_button)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
