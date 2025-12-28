from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QToolButton,
    QButtonGroup,
    QComboBox,
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QPixmap, QCursor


class _ThumbLabel(QLabel):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, pixmap: QPixmap, parent=None):
        super().__init__(parent)
        self.index = index
        self._source_pixmap = pixmap
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setAlignment(Qt.AlignCenter)
        self.setObjectName("thumbLabel")
        self.setScaledContents(False)
        self.update_size(QSize(160, 120))

    def update_size(self, size: QSize):
        self.setFixedSize(size)
        if self._source_pixmap and not self._source_pixmap.isNull():
            self.setPixmap(
                self._source_pixmap.scaled(
                    size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)


class ThumbsWidget(QWidget):
    """
    Right-hand panel with thumbnails and a view-mode toggle.
    """

    thumbnailClicked = pyqtSignal(int)
    viewModeChanged = pyqtSignal(str)
    columnsChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("thumbsWidget")
        self._columns = 2
        self._labels = []

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(10)

        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(8)

        self.original_button = QToolButton()
        self.original_button.setText("Originals")
        self.original_button.setCheckable(True)
        self.original_button.setChecked(True)
        self.original_button.setObjectName("thumbsToggle")
        self.original_button.setProperty("mode", "originals")

        self.converted_button = QToolButton()
        self.converted_button.setText("Converted")
        self.converted_button.setCheckable(True)
        self.converted_button.setEnabled(False)
        self.converted_button.setObjectName("thumbsToggle")
        self.converted_button.setProperty("mode", "converted")

        self._mode_group = QButtonGroup(self)
        self._mode_group.setExclusive(True)
        self._mode_group.addButton(self.original_button)
        self._mode_group.addButton(self.converted_button)
        self._mode_group.buttonClicked.connect(self._on_mode_changed)

        column_label = QLabel("Columns")
        column_label.setObjectName("columnsLabel")

        self.columns_combo = QComboBox()
        self.columns_combo.addItems(["2", "3", "4"])
        self.columns_combo.setCurrentText("2")
        self.columns_combo.currentTextChanged.connect(
            self._on_columns_changed
        )

        header_layout.addWidget(self.original_button)
        header_layout.addWidget(self.converted_button)
        header_layout.addStretch(1)
        header_layout.addWidget(column_label)
        header_layout.addWidget(self.columns_combo)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.inner = QWidget()
        self.grid = QGridLayout(self.inner)
        self.grid.setContentsMargins(6, 6, 6, 6)
        self.grid.setSpacing(8)

        self.scroll.setWidget(self.inner)

        outer_layout.addWidget(header)
        outer_layout.addWidget(self.scroll, stretch=1)

    def set_view_mode(self, mode: str):
        if mode == "converted" and self.converted_button.isEnabled():
            self.converted_button.setChecked(True)
        else:
            self.original_button.setChecked(True)

    def set_converted_enabled(self, enabled: bool):
        self.converted_button.setEnabled(enabled)
        if not enabled and self.converted_button.isChecked():
            self.original_button.setChecked(True)

    def set_columns(self, columns: int):
        columns = max(1, min(6, int(columns)))
        if self._columns == columns:
            return
        self._columns = columns
        self.columns_combo.setCurrentText(str(columns))
        self._relayout()
        self._update_thumb_sizes()
        self.columnsChanged.emit(columns)

    def clear_thumbnails(self):
        for lbl in self._labels:
            lbl.setParent(None)
        self._labels.clear()

    def set_thumbnails(self, pixmaps):
        self.clear_thumbnails()
        for pixmap in pixmaps:
            self._add_thumbnail(pixmap)
        self._relayout()
        self._update_thumb_sizes()

    def _add_thumbnail(self, pixmap: QPixmap):
        index = len(self._labels)
        label = _ThumbLabel(index, pixmap)
        label.clicked.connect(self.thumbnailClicked)
        self._labels.append(label)

    def _relayout(self):
        for i, label in enumerate(self._labels):
            row = i // self._columns
            col = i % self._columns
            self.grid.addWidget(label, row, col)

    def _update_thumb_sizes(self):
        if not self._labels:
            return
        margins = self.grid.contentsMargins()
        spacing = self.grid.spacing()
        available = (
            self.scroll.viewport().width()
            - margins.left()
            - margins.right()
            - spacing * (self._columns - 1)
        )
        if available <= 0:
            size = QSize(140, 105)
        else:
            width = max(110, int(available / self._columns))
            height = int(width * 0.75)
            size = QSize(width, height)
        for label in self._labels:
            label.update_size(size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_thumb_sizes()

    def _on_mode_changed(self, button):
        mode = button.property("mode")
        if mode:
            self.viewModeChanged.emit(mode)

    def _on_columns_changed(self, value):
        try:
            columns = int(value)
        except ValueError:
            return
        if columns != self._columns:
            self._columns = columns
            self._relayout()
            self._update_thumb_sizes()
            self.columnsChanged.emit(columns)
