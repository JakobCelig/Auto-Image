from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ViewerWidget(QFrame):
    """
    Center area that will show the current image
    and a drag & drop hint.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("viewerWidget")
        self.setFrameShape(QFrame.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(12)

        self.title_label = QLabel("Drag & Drop Images")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setObjectName("viewerTitle")

        self.subtitle_label = QLabel(
            "And when they are here → preview of crop..."
        )
        self.subtitle_label.setAlignment(Qt.AlignCenter)
        self.subtitle_label.setObjectName("viewerSubtitle")

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setObjectName("viewerImage")
        self.image_label.setMinimumSize(400, 300)

        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)
        layout.addWidget(self.image_label, stretch=1)

        # Drag & drop can be implemented later
        self.setAcceptDrops(True)

    # Simple API for controller
    def set_image(self, pixmap: QPixmap):
        self.image_label.setPixmap(
            pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
        )

    def clear_image(self):
        self.image_label.clear()
