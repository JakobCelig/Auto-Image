from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap

from widgets.viewer_widget import ViewerWidget


class ViewerController(QObject):
    """
    Controls only the ViewerWidget.
    Other controllers talk to this one, not directly to the widget.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = ViewerWidget()

    # Public API for other controllers
    def show_image(self, pixmap: QPixmap):
        self.widget.set_image(pixmap)

    def clear(self):
        self.widget.clear_image()
