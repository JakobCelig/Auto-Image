from pathlib import Path

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox

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
        self.settings_controller.outputBrowseRequested.connect(
            self._on_output_browse_requested
        )
        self.settings_controller.removeAllRequested.connect(
            self._on_remove_all
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
        output_folder = settings["output_folder"] or "cropped"

        try:
            total = len(images)
            self.settings_controller.start_progress(total)

            def progress_callback(value, total_count):
                self.settings_controller.update_progress(value, total_count)
                QApplication.processEvents()

            outputs, saved_paths = convert_images(
                images,
                threshold=settings["threshold"],
                aspect_w=settings["aspect_w"],
                aspect_h=settings["aspect_h"],
                margin_percent=settings["margin_percent"],
                output_folder=output_folder,
                progress_callback=progress_callback,
            )
        except Exception as exc:
            QMessageBox.warning(
                self.main_widget,
                "Conversion Failed",
                f"Could not convert images: {exc}",
            )
            return
        finally:
            self.settings_controller.finish_progress()

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
            [
                (entry.pixmap, self._name_for_entry(entry, i))
                for i, entry in enumerate(self._converted_entries)
            ]
        )
        self.thumbs_controller.set_view_mode("converted")

    def _add_paths(self, paths):
        file_paths = self._collect_files(paths)
        new_paths = [p for p in file_paths if p not in self._known_paths]
        if not new_paths:
            return

        if self._converted_entries:
            self._converted_entries = []
            self.thumbs_controller.set_converted([])

        total = len(new_paths)
        self.main_widget.start_upload_progress(total)
        loaded_any = False
        self.thumbs_controller.set_view_mode("originals")

        for idx, path in enumerate(new_paths, start=1):
            entries = load_image_entries([path])
            if entries:
                entry = entries[0]
                self._known_paths.add(entry.path)
                self._original_entries.append(entry)
                loaded_any = True

                self.thumbs_controller.add_original(
                    (entry.pixmap, self._name_for_entry(entry, len(self._original_entries) - 1))
                )
                self.viewer_controller.show_image(entry.pixmap)

            self.main_widget.update_upload_progress(idx, total)
            QApplication.processEvents()

        self.main_widget.finish_upload_progress()

        if not loaded_any:
            QMessageBox.information(
                self.main_widget,
                "No Images",
                "None of the selected files could be loaded.",
            )

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

    def _name_for_entry(self, entry: ImageEntry, index: int) -> str:
        if entry.path:
            return Path(entry.path).name
        return f"converted_{index + 1:02d}.png"

    def _on_output_browse_requested(self):
        folder = QFileDialog.getExistingDirectory(
            self.main_widget,
            "Select Output Folder",
            "",
        )
        if folder:
            self.settings_controller.set_output_path(folder)

    def _on_remove_all(self):
        self._original_entries = []
        self._converted_entries = []
        self._known_paths = set()
        self.thumbs_controller.clear()
        self.viewer_controller.clear()
        self.main_widget.finish_upload_progress()
