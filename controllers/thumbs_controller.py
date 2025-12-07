from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QImage

from widgets.thumbs_widget import ThumbsWidget


class ThumbsController(QObject):
    """
    Manages thumbnails list and their widget.
    Exposes thumbnailSelected(index, pixmap) for others.
    """
    thumbnailSelected = pyqtSignal(int, QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = ThumbsWidget()
        self._pixmaps = []

        # Widget -> controller
        self.widget.thumbnailClicked.connect(self._handle_thumb_clicked)

        # Temporary: create some dummy colored thumbnails
        self._create_demo_thumbnails()

    # --- internal helpers -------------------------------------------------

    def _create_demo_thumbnails(self):
        colors = [
            QColor("#4FC3F7"), QColor("#FFB74D"),
            QColor("#81C784"), QColor("#E57373"),
            QColor("#BA68C8"), QColor("#FFF176")
        ]
        for c in colors:
            pm = self._solid_pixmap(240, 160, c)
            self.add_thumbnail(pm)

    @staticmethod
    def _solid_pixmap(w, h, color: QColor) -> QPixmap:
        img = QImage(w, h, QImage.Format_ARGB32)
        img.fill(color)
        return QPixmap.fromImage(img)

    # --- API --------------------------------------------------------------

    def add_thumbnail(self, pixmap: QPixmap):
        self._pixmaps.append(pixmap)
        self.widget.add_thumbnail(pixmap)

    def clear(self):
        self._pixmaps.clear()
        self.widget.clear_thumbnails()

    # --- slots ------------------------------------------------------------

    def _handle_thumb_clicked(self, index: int):
        if 0 <= index < len(self._pixmaps):
            self.thumbnailSelected.emit(index, self._pixmaps[index])
