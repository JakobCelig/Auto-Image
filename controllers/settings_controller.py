from PyQt5.QtCore import QObject

from widgets.settings_widget import SettingsWidget


class SettingsController(QObject):
    """
    Wraps SettingsWidget. Later you connect alpha_slider etc. to real logic.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.widget = SettingsWidget()

        # Example: in the future you might connect:
        # self.widget.alpha_slider.valueChanged.connect(self._on_alpha_changed)

    # def _on_alpha_changed(self, value: int):
    #     ... update model / notify others ...
