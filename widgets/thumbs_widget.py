from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt


class ThumbsWidget(QWidget):
    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)

        title = QLabel("All Uploaded Images")
        title.setAlignment(Qt.AlignCenter)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        grid = QGridLayout(container)

        # 3×3 placeholders
        for row in range(3):
            for col in range(3):
                box = QLabel()
                box.setFixedSize(120, 120)
                box.setStyleSheet("border: 2px solid #666;")
                box.setAlignment(Qt.AlignCenter)
                grid.addWidget(box, row, col)

        scroll.setWidget(container)

        outer.addWidget(title)
        outer.addWidget(scroll)