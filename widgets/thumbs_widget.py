from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QSizePolicy

class ThumbsWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout(self)
        layout.setSpacing(10)

        # create 8 empty preview boxes
        self.thumb_labels = []
        for i in range(8):
            lbl = QLabel()
            lbl.setFixedSize(120, 120)
            lbl.setStyleSheet("border: 2px solid white; background: #222;")
            lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            layout.addWidget(lbl, i // 2, i % 2)
            self.thumb_labels.append(lbl)

        self.setLayout(layout)
