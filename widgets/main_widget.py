from PyQt5.QtWidgets import (
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QSplitter,
    QProgressBar,
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

        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(12)

        left_min_width = max(
            280,
            settings_widget.minimumWidth()
            + left_layout.contentsMargins().left()
            + left_layout.contentsMargins().right(),
        )
        left_frame.setMinimumWidth(left_min_width)
        left_frame.setMaximumWidth(max(320, left_min_width))

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
        right_frame.setMaximumWidth(720)

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
        splitter.setSizes([280, 860, 420])

        root_layout.addWidget(splitter, stretch=1)

        # -------- Status bar (upload progress) --------
        status = self.statusBar()
        status.setObjectName("mainStatus")
        self.upload_progress = QProgressBar()
        self.upload_progress.setObjectName("uploadProgress")
        self.upload_progress.setVisible(False)
        self.upload_progress.setFixedWidth(220)
        self.upload_progress.setTextVisible(True)
        self.upload_progress.setAlignment(Qt.AlignCenter)
        status.addPermanentWidget(self.upload_progress)

    def start_upload_progress(self, total: int):
        total = max(1, total)
        self.upload_progress.setRange(0, total)
        self.upload_progress.setValue(0)
        self.upload_progress.setFormat("Uploading... %p%")
        self.upload_progress.setVisible(True)
        self.statusBar().showMessage("Uploading images...")

    def update_upload_progress(self, value: int, total: int):
        total = max(1, total)
        self.upload_progress.setRange(0, total)
        self.upload_progress.setValue(value)

    def finish_upload_progress(self):
        self.upload_progress.setVisible(False)
        self.statusBar().clearMessage()
