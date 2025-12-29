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
from PyQt5.QtCore import Qt, QTimer
from widgets.ui_scaling import scaled


class MainWidget(QMainWindow):
    def __init__(self, settings_widget: QWidget,
                 viewer_widget: QWidget,
                 thumbs_widget: QWidget,
                 parent=None):
        super().__init__(parent)
        self.setWindowTitle("AutoImage")
        self.setFocusPolicy(Qt.StrongFocus)
        self._settings_widget = settings_widget
        self._thumbs_widget = thumbs_widget

        # ---- Central container ----
        central = QWidget(self)
        self.setCentralWidget(central)

        root_layout = QHBoxLayout(central)
        root_layout.setContentsMargins(
            scaled(10), scaled(10), scaled(10), scaled(10)
        )
        root_layout.setSpacing(scaled(10))

        # -------- LEFT: Settings panel --------
        left_frame = QFrame()
        left_frame.setObjectName("settingsPanel")
        left_frame.setFrameShape(QFrame.NoFrame)

        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(
            scaled(12), scaled(12), scaled(12), scaled(12)
        )
        left_layout.setSpacing(scaled(12))

        left_min_width = max(
            scaled(280),
            settings_widget.minimumWidth()
            + left_layout.contentsMargins().left()
            + left_layout.contentsMargins().right(),
        )
        left_frame.setMinimumWidth(left_min_width)
        left_frame.setMaximumWidth(max(scaled(320), left_min_width))

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
        center_layout.setContentsMargins(
            scaled(12), scaled(12), scaled(12), scaled(12)
        )
        center_layout.setSpacing(scaled(8))

        center_layout.addWidget(viewer_widget, stretch=1)

        # -------- RIGHT: Thumbnails panel --------
        right_frame = QFrame()
        right_frame.setObjectName("thumbsPanel")
        right_frame.setFrameShape(QFrame.NoFrame)

        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(
            scaled(12), scaled(12), scaled(12), scaled(12)
        )
        right_layout.setSpacing(scaled(8))
        right_layout.addWidget(thumbs_widget, stretch=1)
        self._right_layout = right_layout

        right_min_width = self._calc_right_min_width(
            thumbs_widget.minimumWidth()
        )
        right_frame.setMinimumWidth(right_min_width)
        right_frame.setMaximumWidth(max(scaled(720), right_min_width))
        self._right_frame = right_frame

        # -------- Add to root layout --------
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.addWidget(left_frame)
        splitter.addWidget(center_frame)
        splitter.addWidget(right_frame)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)
        splitter.setSizes([scaled(280), scaled(860), right_min_width])
        self._splitter = splitter
        if hasattr(thumbs_widget, "minimumWidthChanged"):
            thumbs_widget.minimumWidthChanged.connect(
                self._sync_thumbs_min_width
            )

        root_layout.addWidget(splitter, stretch=1)

        # -------- Status bar (upload progress) --------
        status = self.statusBar()
        status.setObjectName("mainStatus")
        self.upload_progress = QProgressBar()
        self.upload_progress.setObjectName("uploadProgress")
        self.upload_progress.setVisible(False)
        self.upload_progress.setFixedWidth(scaled(220))
        self.upload_progress.setTextVisible(True)
        self.upload_progress.setAlignment(Qt.AlignCenter)
        status.addPermanentWidget(self.upload_progress)
        QTimer.singleShot(0, self._clear_initial_focus)

    def _clear_initial_focus(self):
        self.setFocus(Qt.OtherFocusReason)
        if hasattr(self._settings_widget, "clear_focus_state"):
            self._settings_widget.clear_focus_state()
        self._sync_thumbs_min_width(self._thumbs_widget.minimumWidth())

    def _calc_right_min_width(self, thumbs_min_width: int) -> int:
        margins = self._right_layout.contentsMargins()
        return max(
            scaled(160),
            int(thumbs_min_width) + margins.left() + margins.right(),
        )

    def _sync_thumbs_min_width(self, thumbs_min_width: int):
        right_min_width = self._calc_right_min_width(thumbs_min_width)
        if right_min_width == self._right_frame.minimumWidth():
            return
        self._right_frame.setMinimumWidth(right_min_width)
        self._right_frame.setMaximumWidth(max(scaled(720), right_min_width))
        sizes = self._splitter.sizes()
        if sizes and sizes[-1] < right_min_width:
            diff = right_min_width - sizes[-1]
            sizes[-1] = right_min_width
            take = min(diff, sizes[1])
            sizes[1] -= take
            diff -= take
            if diff > 0:
                sizes[0] = max(0, sizes[0] - diff)
            self._splitter.setSizes(sizes)

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
