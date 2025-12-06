# controllers/thumbs_controller.py

class ThumbsController:
    def __init__(self, widget):
        self.widget = widget

        # initially empty
        self.images = []

    def set_images(self, images):
        self.images = images
        self.widget.update_thumbnails(images)
