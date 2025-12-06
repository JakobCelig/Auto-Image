class MainController:
    def __init__(self, widget):
        self.widget = widget

        # connect signals
        self.widget.load_button.clicked.connect(self.load_images)
        self.widget.crop_button.clicked.connect(self.crop_images)

    def load_images(self):
        self.widget.status_label.setText("Load clicked!")

    def crop_images(self):
        self.widget.status_label.setText("Crop clicked!")