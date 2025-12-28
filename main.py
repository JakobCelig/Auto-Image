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
    custom_css = """
    QFrame#settingsPanel, QFrame#viewerPanel, QFrame#thumbsPanel {
        background-color: #151A23;
        border-radius: 14px;
    }

    QLabel#panelTitle {
        color: #E2E8F0;
        font-size: 15px;
        font-weight: 600;
        padding-bottom: 4px;
    }

    QLabel#viewerTitle {
        color: #E2E8F0;
        font-size: 16px;
        font-weight: 600;
    }

    QLabel#viewerSubtitle, QLabel#settingsHint {
        color: #9AA4B2;
    }

    QFrame#dropArea {
        background-color: #11161E;
        border: 1px dashed #2B3745;
        border-radius: 14px;
    }

    QLabel#thumbLabel {
        background-color: #0F141B;
        border: 1px solid #273241;
        border-radius: 10px;
    }

    QLabel#thumbLabel:hover {
        border-color: #3B485C;
    }

    QToolButton#thumbsToggle {
        background-color: #1B2430;
        border: 1px solid #2B3745;
        border-radius: 10px;
        padding: 6px 12px;
        color: #CDD6E0;
    }

    QToolButton#thumbsToggle:checked {
        background-color: #2B6CB0;
        border-color: #2B6CB0;
        color: #F8FAFC;
    }

    QPushButton#convertButton {
        background-color: #1D8A7A;
        border-radius: 12px;
        padding: 10px;
        font-weight: 600;
        color: #F8FAFC;
    }

    QPushButton#convertButton:hover {
        background-color: #21A693;
    }
    """

    apply_stylesheet(app, theme='dark_blue.xml')
    app.setStyleSheet(app.styleSheet() + custom_css)

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
