from pathlib import Path

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from controllers.viewer_controller import ViewerController
from controllers.thumbs_controller import ThumbsController
from controllers.settings_controller import SettingsController
from controllers.image_processing import (
    ImageEntry,
    load_image_entries,
    convert_images,
    pixmap_from_bgr,
)
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
        self._original_entries = []
        self._converted_entries = []
        self._known_paths = set()

        self.thumbs_controller.thumbnailSelected.connect(
            self._on_thumbnail_selected
        )
        self.viewer_controller.filesDropped.connect(self._on_files_dropped)
        self.viewer_controller.browseRequested.connect(self._on_browse_requested)
        self.settings_controller.convertRequested.connect(
            self._on_convert_requested
        )

    def _on_thumbnail_selected(self, index, pixmap, mode):
        self.viewer_controller.show_image(pixmap)

    def _on_browse_requested(self):
        files, _ = QFileDialog.getOpenFileNames(
            self.main_widget,
            "Add Images",
            "",
            "All files (*);;Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)",
        )
        if files:
            self._add_paths(files)

    def _on_files_dropped(self, paths):
        if paths:
            self._add_paths(paths)

    def _on_convert_requested(self):
        if not self._original_entries:
            QMessageBox.information(
                self.main_widget,
                "No Images",
                "Add some images before converting.",
            )
            return

        settings = self.settings_controller.get_settings()
        images = [entry.cv_image for entry in self._original_entries]

        try:
            outputs, saved_paths = convert_images(
                images,
                threshold=settings["threshold"],
                aspect_w=settings["aspect_w"],
                aspect_h=settings["aspect_h"],
                margin_percent=settings["margin_percent"],
                output_folder="cropped",
            )
        except Exception as exc:
            QMessageBox.warning(
                self.main_widget,
                "Conversion Failed",
                f"Could not convert images: {exc}",
            )
            return

        if not outputs:
            QMessageBox.warning(
                self.main_widget,
                "Conversion Failed",
                "No outputs were generated.",
            )
            return

        converted_entries = []
        for i, img in enumerate(outputs):
            path = saved_paths[i] if i < len(saved_paths) else ""
            pixmap = pixmap_from_bgr(img)
            converted_entries.append(
                ImageEntry(path=path, pixmap=pixmap, cv_image=img)
            )

        self._converted_entries = converted_entries
        self.thumbs_controller.set_converted(
            [entry.pixmap for entry in self._converted_entries]
        )
        self.thumbs_controller.set_view_mode("converted")

    def _add_paths(self, paths):
        file_paths = self._collect_files(paths)
        new_paths = [p for p in file_paths if p not in self._known_paths]
        if not new_paths:
            return

        entries = load_image_entries(new_paths)
        if not entries:
            QMessageBox.information(
                self.main_widget,
                "No Images",
                "None of the selected files could be loaded.",
            )
            return

        if self._converted_entries:
            self._converted_entries = []
            self.thumbs_controller.set_converted([])

        for entry in entries:
            self._known_paths.add(entry.path)
        self._original_entries.extend(entries)

        self.thumbs_controller.set_originals(
            [entry.pixmap for entry in self._original_entries]
        )
        self.thumbs_controller.set_view_mode("originals")
        self.viewer_controller.show_image(entries[-1].pixmap)

    def _collect_files(self, paths):
        files = []
        for raw in paths:
            path = Path(raw)
            if path.is_dir():
                for item in path.iterdir():
                    if item.is_file():
                        files.append(str(item))
            elif path.is_file():
                files.append(str(path))
        return files
