from PyQt5.QtWidgets import (
    QWidget,
    QScrollArea,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QHBoxLayout,
    QCheckBox,
    QFrame,
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRectF, QEvent
from PyQt5.QtGui import QPixmap, QCursor, QPainter, QColor, QPen
from widgets.ui_scaling import scaled


class ToggleSwitch(QCheckBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("thumbsSwitch")
        self.setFixedSize(scaled(46), scaled(24))
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.NoFocus)
        self._margin = scaled(3)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(1, 1, self.width() - 2, self.height() - 2)
        checked = self.isChecked()

        if not self.isEnabled():
            track_color = QColor("#11161E")
            border_color = QColor("#243040")
            knob_color = QColor("#566172")
        else:
            track_color = QColor("#5C6BC0") if checked else QColor("#1B2430")
            border_color = QColor("#5C6BC0") if checked else QColor("#2B3745")
            knob_color = QColor("#F8FAFC")

        painter.setPen(QPen(border_color, scaled(1)))
        painter.setBrush(track_color)
        painter.drawRoundedRect(rect, rect.height() / 2, rect.height() / 2)

        knob_diam = rect.height() - 2 * self._margin
        knob_x = (
            rect.right() - self._margin - knob_diam
            if checked
            else rect.left() + self._margin
        )
        painter.setPen(Qt.NoPen)
        painter.setBrush(knob_color)
        painter.drawEllipse(
            QRectF(
                knob_x,
                rect.top() + self._margin,
                knob_diam,
                knob_diam,
            )
        )

    def hitButton(self, pos):
        return self.rect().contains(pos)


class _ThumbItem(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, pixmap: QPixmap, name: str, parent=None):
        super().__init__(parent)
        self.index = index
        self._name = name
        self._source_pixmap = pixmap
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setObjectName("thumbItem")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            scaled(6), scaled(6), scaled(6), scaled(6)
        )
        layout.setSpacing(scaled(6))

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setObjectName("thumbImage")
        self.image_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        self.name_label = QLabel(name)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setObjectName("thumbName")
        self.name_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.name_label.setWordWrap(False)

        layout.addWidget(self.image_label)
        layout.addWidget(self.name_label)

        self.update_size(QSize(scaled(160), scaled(120)))

    def update_size(self, size: QSize):
        self.image_label.setFixedSize(size)
        if self._source_pixmap and not self._source_pixmap.isNull():
            self.image_label.setPixmap(
                self._source_pixmap.scaled(
                    size, Qt.KeepAspectRatio, Qt.SmoothTransformation
                )
            )
        total_height = size.height() + scaled(34)
        self.setFixedSize(size.width() + scaled(12), total_height)
        self.name_label.setFixedWidth(size.width())
        self._apply_name_elide(size.width())

    def _apply_name_elide(self, width: int):
        metrics = self.name_label.fontMetrics()
        elided = metrics.elidedText(self._name, Qt.ElideRight, width)
        self.name_label.setText(elided)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.rect().contains(event.pos()):
            self.clicked.emit(self.index)
        super().mouseReleaseEvent(event)


class ThumbsWidget(QWidget):
    """
    Right-hand panel with thumbnails and a view-mode toggle.
    """

    selectionChanged = pyqtSignal(int)
    viewModeChanged = pyqtSignal(str)
    minimumWidthChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("thumbsWidget")
        self._columns = 2
        self._labels = []
        self._min_thumb_width = scaled(150)
        self._max_columns = 3
        self._selected_index = -1

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(scaled(10))
        self.setFocusPolicy(Qt.StrongFocus)

        self.header = QWidget()
        self.header.setObjectName("thumbsHeader")
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        self.header_layout.setSpacing(scaled(8))

        self.original_label = QLabel("Originals")
        self.original_label.setObjectName("thumbsModeLabel")

        self.mode_switch = ToggleSwitch()
        self.mode_switch.setChecked(False)
        self.mode_switch.setEnabled(False)
        self.mode_switch.stateChanged.connect(self._on_mode_toggled)

        self.converted_label = QLabel("Converted")
        self.converted_label.setObjectName("thumbsModeLabel")

        self.header_layout.addWidget(self.original_label)
        self.header_layout.addWidget(self.mode_switch)
        self.header_layout.addWidget(self.converted_label)
        self.header_layout.addStretch(1)

        self.scroll = QScrollArea()
        self.scroll.setObjectName("thumbsScroll")
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)

        self.inner = QWidget()
        self.grid = QGridLayout(self.inner)
        self.grid.setContentsMargins(
            scaled(6), scaled(6), scaled(6), scaled(6)
        )
        self.grid.setSpacing(scaled(8))
        self.grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.scroll.setWidget(self.inner)

        outer_layout.addWidget(self.header)
        outer_layout.addWidget(self.scroll, stretch=1)
        self._update_minimum_width()

    def set_view_mode(self, mode: str):
        if mode == "converted" and self.mode_switch.isEnabled():
            self.mode_switch.setChecked(True)
        else:
            self.mode_switch.setChecked(False)

    def _update_minimum_width(self):
        spacing = self.header_layout.spacing()
        margins = self.header_layout.contentsMargins()
        original_width = self.original_label.sizeHint().width()
        converted_width = self.converted_label.sizeHint().width()
        self.original_label.setMinimumWidth(original_width)
        self.converted_label.setMinimumWidth(converted_width)
        extra = scaled(12)
        header_width = (
            original_width
            + self.mode_switch.sizeHint().width()
            + converted_width
            + spacing * 3
            + margins.left()
            + margins.right()
            + extra
        )
        new_min_width = max(scaled(160), header_width)
        if new_min_width != self.minimumWidth():
            self.setMinimumWidth(new_min_width)
            self.minimumWidthChanged.emit(new_min_width)

    def changeEvent(self, event):
        super().changeEvent(event)
        if event.type() in (QEvent.FontChange, QEvent.StyleChange):
            self._update_minimum_width()

    def set_converted_enabled(self, enabled: bool):
        self.mode_switch.setEnabled(enabled)
        self.converted_label.setEnabled(enabled)
        if not enabled and self.mode_switch.isChecked():
            self.mode_switch.setChecked(False)

    def clear_thumbnails(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
        self._labels.clear()
        self._selected_index = -1

    def set_thumbnails(self, items):
        self.clear_thumbnails()
        for pixmap, name in items:
            self._add_thumbnail(pixmap, name)
        self._update_layout()
        if self._labels:
            self.set_selected_index(0, emit_signal=False)

    def add_thumbnail(self, pixmap: QPixmap, name: str):
        self._add_thumbnail(pixmap, name)
        self._update_layout()

    def _add_thumbnail(self, pixmap: QPixmap, name: str):
        index = len(self._labels)
        label = _ThumbItem(index, pixmap, name)
        label.clicked.connect(self._handle_thumb_clicked)
        self._labels.append(label)

    def _relayout(self):
        for label in self._labels:
            self.grid.removeWidget(label)
        for i, label in enumerate(self._labels):
            row = i // self._columns
            col = i % self._columns
            self.grid.addWidget(label, row, col)
        self._apply_row_stretch()

    def _apply_row_stretch(self):
        if not self._labels:
            return
        last_row = (len(self._labels) - 1) // self._columns
        for row in range(self.grid.rowCount() + 2):
            self.grid.setRowStretch(row, 0)
        self.grid.setRowStretch(last_row + 1, 1)

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
            size = QSize(scaled(140), scaled(105))
        else:
            width = max(
                scaled(110), int(available / self._columns) - scaled(12)
            )
            height = int(width * 0.75)
            size = QSize(width, height)
        for label in self._labels:
            label.update_size(size)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_layout()

    def _update_layout(self):
        if not self._labels:
            return
        columns = self._calculate_columns()
        self._columns = columns
        self._relayout()
        self._update_thumb_sizes()
        self.inner.adjustSize()

    def _calculate_columns(self):
        margins = self.grid.contentsMargins()
        spacing = self.grid.spacing()
        available = (
            self.scroll.viewport().width()
            - margins.left()
            - margins.right()
        )
        if available <= 0:
            return 1

        min_cell = self._min_thumb_width + scaled(12)
        columns = int((available + spacing) / (min_cell + spacing))
        columns = max(1, min(self._max_columns, columns))
        return min(columns, max(1, len(self._labels)))

    def _on_mode_toggled(self, state):
        mode = "converted" if state == Qt.Checked else "originals"
        self.viewModeChanged.emit(mode)

    def _handle_thumb_clicked(self, index: int):
        self.setFocus(Qt.MouseFocusReason)
        self.set_selected_index(index, emit_signal=True)

    def set_selected_index(self, index: int, emit_signal: bool = False):
        if not self._labels:
            self._selected_index = -1
            return
        index = max(0, min(index, len(self._labels) - 1))
        if index == self._selected_index:
            return
        if 0 <= self._selected_index < len(self._labels):
            self._set_label_selected(self._labels[self._selected_index], False)
        self._selected_index = index
        label = self._labels[index]
        self._set_label_selected(label, True)
        self.scroll.ensureWidgetVisible(label)
        if emit_signal:
            self.selectionChanged.emit(index)

    def _set_label_selected(self, label: _ThumbItem, selected: bool):
        label.setProperty("selected", selected)
        label.style().unpolish(label)
        label.style().polish(label)
        label.update()

    def keyPressEvent(self, event):
        if not self._labels:
            super().keyPressEvent(event)
            return

        key = event.key()
        index = self._selected_index if self._selected_index >= 0 else 0
        new_index = index
        count = len(self._labels)

        if key == Qt.Key_Left:
            new_index = max(0, index - 1)
        elif key == Qt.Key_Right:
            new_index = min(count - 1, index + 1)
        elif key == Qt.Key_Up:
            new_index = index - self._columns
        elif key == Qt.Key_Down:
            new_index = index + self._columns
        else:
            super().keyPressEvent(event)
            return

        if 0 <= new_index < count:
            self.set_selected_index(new_index, emit_signal=True)
