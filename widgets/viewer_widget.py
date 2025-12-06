from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt

class ViewerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

        layout = QVBoxLayout(self)
        self.info = QLabel("Drag & Drop images here\nPreview of crop will appear…")
        self.info.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.info)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        paths = [u.toLocalFile() for u in urls]
        self.info.setText("\n".join(paths))
