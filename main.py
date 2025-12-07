import sys
from PyQt5.QtWidgets import QApplication
from qt_material import apply_stylesheet

from widgets.main_widget import MainWidget
from controllers.main_controller import MainController
from controllers.viewer_controller import ViewerController
from controllers.thumbs_controller import ThumbsController
from controllers.settings_controller import SettingsController


def main():
    app = QApplication(sys.argv)

    # Modern dark theme (change name if you prefer another qt-material theme)
    apply_stylesheet(app, theme='dark_blue.xml')

    # --- Create controllers (each one owns its widget) ---
    viewer_controller = ViewerController()
    thumbs_controller = ThumbsController()
    settings_controller = SettingsController()

    # --- Create main window and pass only widgets in ---
    main_window = MainWidget(
        settings_widget=settings_controller.widget,
        viewer_widget=viewer_controller.widget,
        thumbs_widget=thumbs_controller.widget,
    )

    # --- Wire everything through MainController (controllers only) ---
    main_controller = MainController(
        main_widget=main_window,
        viewer_controller=viewer_controller,
        thumbs_controller=thumbs_controller,
        settings_controller=settings_controller,
    )

    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
