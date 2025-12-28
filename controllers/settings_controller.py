from PyQt5.QtCore import QObject, pyqtSignal

from widgets.settings_widget import SettingsWidget


class SettingsController(QObject):
    """
    Wraps SettingsWidget and exposes settings for conversion.
    """
    convertRequested = pyqtSignal()
    outputBrowseRequested = pyqtSignal()
    removeAllRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = SettingsWidget()

        self.widget.convert_button.clicked.connect(self.convertRequested)
        self.widget.output_browse_button.clicked.connect(
            self.outputBrowseRequested
        )
        self.widget.remove_button.clicked.connect(self.removeAllRequested)

    def get_settings(self):
        return {
            "threshold": int(self.widget.threshold_spin.value()),
            "margin_percent": float(self.widget.margin_spin.value()) / 100.0,
            "aspect_w": int(self.widget.aspect_w_spin.value()),
            "aspect_h": int(self.widget.aspect_h_spin.value()),
            "output_folder": self.widget.output_path_label.text().strip(),
        }

    def set_output_path(self, path: str):
        self.widget.output_path_label.setText(path)

    def start_progress(self, total: int):
        self.widget.progress_bar.setRange(0, max(1, total))
        self.widget.progress_bar.setValue(0)
        self.widget.progress_bar.setFormat("Converting... 0%")
        self.widget.convert_stack.setCurrentWidget(self.widget.progress_bar)

    def update_progress(self, value: int, total: int):
        total = max(1, total)
        self.widget.progress_bar.setRange(0, total)
        self.widget.progress_bar.setValue(value)
        percent = int((value / total) * 100)
        self.widget.progress_bar.setFormat(f"Converting... {percent}%")

    def finish_progress(self):
        self.widget.convert_stack.setCurrentWidget(self.widget.convert_button)
