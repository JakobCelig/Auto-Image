from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QSplitter,
)
from PyQt5.QtCore import Qt


class MainWidget(QMainWindow):
    def __init__(self, settings_widget: QWidget,
                 viewer_widget: QWidget,
                 thumbs_widget: QWidget,
                 parent=None):
        super().__init__(parent)
        self.setWindowTitle("AutoImage")

        # ---- Central container ----
        central = QWidget(self)
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(10, 10, 10, 10)
        root_layout.setSpacing(10)

        # -------- LEFT: Settings panel --------
        left_frame = QFrame()
        left_frame.setObjectName("settingsPanel")
        left_frame.setFrameShape(QFrame.NoFrame)
        left_frame.setMinimumWidth(240)
        left_frame.setMaximumWidth(320)

        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(12)

        left_title = QLabel("Image Settings")
        left_title.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        left_title.setObjectName("panelTitle")

        left_layout.addWidget(left_title)
        left_layout.addWidget(settings_widget, stretch=1)

        # -------- CENTER: Viewer panel --------
        center_frame = QFrame()
        center_frame.setObjectName("viewerPanel")
        center_frame.setFrameShape(QFrame.NoFrame)

        center_layout = QVBoxLayout(center_frame)
        center_layout.setContentsMargins(12, 12, 12, 12)
        center_layout.setSpacing(8)

        center_layout.addWidget(viewer_widget, stretch=1)

        # -------- RIGHT: Thumbnails panel --------
        right_frame = QFrame()
        right_frame.setObjectName("thumbsPanel")
        right_frame.setFrameShape(QFrame.NoFrame)
        right_frame.setMinimumWidth(280)
        right_frame.setMaximumWidth(420)

        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(12, 12, 12, 12)
        right_layout.setSpacing(8)
        right_layout.addWidget(thumbs_widget, stretch=1)

        # -------- Add to root layout --------
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(left_frame)
        splitter.addWidget(center_frame)
        splitter.addWidget(right_frame)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([280, 900, 340])

        root_layout.addWidget(splitter, stretch=1)
