# controllers/settings_controller.py

class SettingsController:
    def __init__(self, widget, main_controller=None):
        self.widget = widget
        self.main_controller = main_controller  # optional link

        # connect UI events
        self.widget.alpha_slider.valueChanged.connect(self._alpha_changed)

    def _alpha_changed(self, value):
        self.widget.alpha_value_label.setText(str(value))

        # TODO: send value to main controller if needed
        print("Alpha changed:", value)
