from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap, QPen, QColor
from widgets.ui_scaling import scaled


class ImageDropArea(QFrame):
    """
    Drag & drop area that keeps the aspect ratio of the current image.
    """

    filesDropped = pyqtSignal(list)
    browseRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("dropArea")
        self.setFrameShape(QFrame.NoFrame)
        self.setAcceptDrops(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(scaled(360), scaled(260))
        self.setAttribute(Qt.WA_StyledBackground, True)

        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

        self._pixmap = None
        self._aspect_ratio = 1.0
        self._drag_active = False

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        if self._aspect_ratio <= 0:
            return width
        return int(width / self._aspect_ratio)

    def set_pixmap(self, pixmap: QPixmap):
        self._pixmap = pixmap
        if pixmap and not pixmap.isNull():
            self._aspect_ratio = pixmap.width() / pixmap.height()
        else:
            self._aspect_ratio = 1.0
        self.updateGeometry()
        self.update()

    def clear_pixmap(self):
        self._pixmap = None
        self._aspect_ratio = 1.0
        self.updateGeometry()
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self._drag_active = True
            self.update()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self._drag_active = False
        self.update()
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        self._drag_active = False
        urls = event.mimeData().urls()
        paths = [url.toLocalFile() for url in urls if url.isLocalFile()]
        if paths:
            self.filesDropped.emit(paths)
        event.acceptProposedAction()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.browseRequested.emit()
        super().mousePressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = self.contentsRect().adjusted(
            scaled(16), scaled(16), -scaled(16), -scaled(16)
        )
        if self._pixmap and not self._pixmap.isNull():
            scaled_pixmap = self._pixmap.scaled(
                rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            x = rect.x() + (rect.width() - scaled_pixmap.width()) // 2
            y = rect.y() + (rect.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(x, y, scaled_pixmap)
            return

        pen_color = QColor("#7C8797" if not self._drag_active else "#9AD0FF")
        painter.setPen(QPen(pen_color, scaled(1)))
        painter.drawRoundedRect(rect, scaled(10), scaled(10))

        painter.setPen(QColor("#B5BDC9"))
        text = "Drop images here\nor click to browse"
        painter.drawText(rect, Qt.AlignCenter, text)


class ViewerWidget(QFrame):
    """
    Center preview panel with a drop area.
    """

    filesDropped = pyqtSignal(list)
    browseRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("viewerWidget")
        self.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            scaled(16), scaled(16), scaled(16), scaled(16)
        )
        layout.setSpacing(scaled(12))

        self.title_label = QLabel("Preview")
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setObjectName("viewerTitle")


        self.drop_area = ImageDropArea()
        self.drop_area.filesDropped.connect(self.filesDropped)
        self.drop_area.browseRequested.connect(self.browseRequested)

        layout.addWidget(self.title_label)
        layout.addWidget(self.drop_area, stretch=1)

    def set_image(self, pixmap: QPixmap):
        self.drop_area.set_pixmap(pixmap)

    def clear_image(self):
        self.drop_area.clear_pixmap()
