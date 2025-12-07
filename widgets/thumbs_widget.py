from PyQt5.QtWidgets import (
    QWidget, QScrollArea, QVBoxLayout, QLabel, QGridLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QCursor


class _ThumbLabel(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.index = index
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("thumbLabel")
        self.setMinimumSize(120, 90)
        self.setMaximumHeight(120)
        self.setScaledContents(True)
        self.setPixmap(
            pixmap.scaled(
                180, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)


class ThumbsWidget(QWidget):
    """
    Right-hand panel with thumbnails arranged 2xN.
    Emits thumbnailClicked(index) when user clicks a thumbnail.
    """
    thumbnailClicked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("thumbsWidget")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.inner = QWidget()
        self.grid = QGridLayout(self.inner)
        self.grid.setContentsMargins(4, 4, 4, 4)
        self.grid.setSpacing(6)

        self.scroll.setWidget(self.inner)
        outer_layout.addWidget(self.scroll)

        self._labels = []

    def clear_thumbnails(self):
        for lbl in self._labels:
            lbl.setParent(None)
        self._labels.clear()

    def add_thumbnail(self, pixmap: QPixmap):
        index = len(self._labels)
        label = _ThumbLabel(index, pixmap)
        label.clicked.connect(self.thumbnailClicked)

        row = index // 2  # 2 columns
        col = index % 2
        self.grid.addWidget(label, row, col)
        self._labels.append(label)
