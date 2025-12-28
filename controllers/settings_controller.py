from PyQt5.QtCore import QObject, pyqtSignal

from widgets.settings_widget import SettingsWidget


class SettingsController(QObject):
    """
    Wraps SettingsWidget and exposes settings for conversion.
    """
    convertRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = SettingsWidget()

        self.widget.convert_button.clicked.connect(self.convertRequested)

    def get_settings(self):
        return {
            "threshold": int(self.widget.threshold_spin.value()),
            "margin_percent": float(self.widget.margin_spin.value()) / 100.0,
            "aspect_w": int(self.widget.aspect_w_spin.value()),
            "aspect_h": int(self.widget.aspect_h_spin.value()),
        }
