from PyQt5.QtCore import QObject

from controllers.viewer_controller import ViewerController
from controllers.thumbs_controller import ThumbsController
from controllers.settings_controller import SettingsController
from widgets.main_widget import MainWidget


class MainController(QObject):
    """
    Orchestrates high-level behaviour.
    Talks only to controllers, not to widgets.
    """
    def __init__(
        self,
        main_widget: MainWidget,
        viewer_controller: ViewerController,
        thumbs_controller: ThumbsController,
        settings_controller: SettingsController,
        parent=None,
    ):
        super().__init__(parent)

        self.main_widget = main_widget
        self.viewer_controller = viewer_controller
        self.thumbs_controller = thumbs_controller
        self.settings_controller = settings_controller

        # Example wiring:
        # when a thumbnail is selected, show it in the viewer
        self.thumbs_controller.thumbnailSelected.connect(
            self._on_thumbnail_selected
        )

        # You can also listen to settings changes later and update others.

    # --- slots ------------------------------------------------------------

    def _on_thumbnail_selected(self, index, pixmap):
        # High-level decision: simply show the image in the viewer
        self.viewer_controller.show_image(pixmap)
