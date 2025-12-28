from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

from widgets.thumbs_widget import ThumbsWidget


class ThumbsController(QObject):
    """
    Manages thumbnails list and their widget.
    Exposes thumbnailSelected(index, pixmap, mode) for others.
    """

    thumbnailSelected = pyqtSignal(int, QPixmap, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = ThumbsWidget()
        self._mode = "originals"
        self._originals = []
        self._converted = []

        self.widget.selectionChanged.connect(self._handle_selection_changed)
        self.widget.viewModeChanged.connect(self._handle_mode_changed)

    def set_originals(self, items):
        self._originals = list(items)
        if self._mode == "originals":
            self.widget.set_thumbnails(self._originals)

    def add_original(self, item):
        self._originals.append(item)
        if self._mode == "originals":
            self.widget.add_thumbnail(item[0], item[1])
            self.widget.set_selected_index(len(self._originals) - 1, True)

    def set_converted(self, items):
        self._converted = list(items)
        self.widget.set_converted_enabled(bool(self._converted))
        if self._mode == "converted":
            self.widget.set_thumbnails(self._converted)

    def clear(self):
        self._originals.clear()
        self._converted.clear()
        self.widget.set_converted_enabled(False)
        self.widget.set_thumbnails([])
        self._mode = "originals"
        self.widget.set_view_mode(self._mode)

    def set_view_mode(self, mode: str):
        if mode not in ("originals", "converted"):
            return
        if mode == "converted" and not self._converted:
            mode = "originals"
        if self._mode == mode:
            return
        self._mode = mode
        self.widget.set_view_mode(mode)
        self._apply_view()

    def _apply_view(self):
        if self._mode == "converted":
            self.widget.set_thumbnails(self._converted)
        else:
            self.widget.set_thumbnails(self._originals)
        self._emit_first_if_any()

    def _emit_first_if_any(self):
        current = self._converted if self._mode == "converted" else self._originals
        if current:
            self.thumbnailSelected.emit(0, current[0][0], self._mode)

    def _handle_thumb_clicked(self, index: int):
        current = self._converted if self._mode == "converted" else self._originals
        if 0 <= index < len(current):
            self.thumbnailSelected.emit(index, current[index][0], self._mode)

    def _handle_selection_changed(self, index: int):
        self._handle_thumb_clicked(index)

    def _handle_mode_changed(self, mode: str):
        if mode == self._mode:
            return
        if mode == "converted" and not self._converted:
            self.widget.set_view_mode("originals")
            return
        self._mode = mode
        self._apply_view()
