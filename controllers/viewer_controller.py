# controllers/viewer_controller.py

class ViewerController:
    def __init__(self, widget):
        self.widget = widget

    def show_image(self, img):
        self.widget.set_image(img)
