from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel,
    QSplitter, QSizePolicy
)
from PyQt5.QtCore import Qt

from widgets.settings_widget import SettingsWidget
from widgets.viewer_widget import ViewerWidget
from widgets.thumbs_widget import ThumbsWidget


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AutoImage")
        self.setMinimumSize(1200, 700)

        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)

        # LEFT PANEL – settings
        self.settings_panel = SettingsWidget()
        splitter.addWidget(self.settings_panel)

        # CENTER PANEL – drag and drop viewer
        self.viewer_panel = ViewerWidget()
        splitter.addWidget(self.viewer_panel)

        # RIGHT PANEL – thumbnails
        self.thumbs_panel = ThumbsWidget()
        splitter.addWidget(self.thumbs_panel)

        # Default sizes
        splitter.setSizes([250, 700, 300])

        main_layout.addWidget(splitter)
