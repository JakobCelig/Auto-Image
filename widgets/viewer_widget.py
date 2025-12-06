from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class ViewerWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        label = QLabel(
            "<h2>Drag & Drop Images</h2>"
            "<p>And when they are here → preview of crop...</p>"
        )
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)

        layout.addWidget(label)
