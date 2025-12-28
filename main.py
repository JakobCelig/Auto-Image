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
        border-radius: 16px;
    }

    QFrame#thumbItem {
        background-color: #0F141B;
        border: 1px solid #273241;
        border-radius: 12px;
    }

    QFrame#thumbItem:hover {
        border-color: #3B485C;
    }

    QFrame#thumbItem[selected="true"] {
        border: 2px solid #5C6BC0;
    }

    QLabel#thumbName {
        color: #8C97A5;
        font-size: 11px;
    }

    QLabel#thumbsModeLabel {
        color: #CDD6E0;
        font-size: 12px;
    }

    QLabel#thumbsModeLabel:disabled {
        color: #6E7A8B;
    }

    QScrollArea#thumbsScroll,
    QScrollArea#thumbsScroll QWidget#qt_scrollarea_viewport,
    QScrollArea#thumbsScroll QWidget#qt_scrollarea_viewport > QWidget,
    QWidget#thumbsHeader {
        background: transparent;
        border: none;
    }

    QAbstractSpinBox {
        background-color: #2A2F36;
        border: 1px solid #3A4454;
        border-bottom: 1px solid #3A4454;
        border-radius: 14px;
        padding: 8px 12px;
        color: #E6EBF2;
    }

    QAbstractSpinBox:hover {
        border-color: #495469;
    }

    QAbstractSpinBox:focus {
        border: 1px solid #3A4454;
        border-bottom: 2px solid #5C6BC0;
        background-color: #2A2F36;
    }

    QAbstractSpinBox::lineEdit {
        background: transparent;
        border: none;
        padding: 0;
    }

    QLabel#ratioSeparator {
        color: #A7B0BE;
    }

    QWidget#aspectRow,
    QWidget#outputSection,
    QWidget#outputHeader,
    QWidget#outputRow {
        background: transparent;
        border: none;
    }

    QLabel#outputPath {
        color: #D3D8E0;
        padding: 8px 12px;
        border: 1px solid #3A4454;
        border-bottom: 1px solid #3A4454;
        border-radius: 14px;
        background-color: #151A23;
    }

    QToolButton#outputBrowse {
        background-color: #2A2F36;
        border: 1px solid #3A4454;
        border-radius: 14px;
        padding: 8px 12px;
        color: #E6EBF2;
    }

    QToolButton#outputBrowse:hover {
        background-color: #2E343C;
        border-bottom: 2px solid #5C6BC0;
    }

    QPushButton#convertButton {
        background-color: #5C6BC0;
        border: 1px solid #5C6BC0;
        border-radius: 12px;
        padding: 8px 12px;
        font-weight: 600;
        color: #F8FAFC;
    }

    QPushButton#convertButton:hover {
        background-color: #6F7EDD;
        border-color: #6F7EDD;
    }

    QPushButton#removeButton {
        background-color: transparent;
        border: 1px solid #4C5AA6;
        border-radius: 12px;
        padding: 8px 12px;
        color: #BFC6F8;
    }

    QPushButton#removeButton:hover {
        background-color: #242C4E;
        border-color: #5C6BC0;
    }

    QProgressBar#convertProgress {
        border: 1px solid #2B3745;
        border-radius: 12px;
        background-color: #0F141B;
        text-align: center;
        color: #F8FAFC;
        height: 38px;
    }

    QProgressBar#convertProgress::chunk {
        background-color: #2B6CB0;
        border-radius: 12px;
    }

    QStackedWidget#convertStack {
        background: transparent;
        border: none;
    }

    QStatusBar#mainStatus {
        background-color: #0E131A;
        color: #9AA4B2;
    }

    QProgressBar#uploadProgress {
        border: 1px solid #2B3745;
        border-radius: 10px;
        background-color: #11161E;
        text-align: center;
        color: #F8FAFC;
        height: 18px;
    }

    QProgressBar#uploadProgress::chunk {
        background-color: #1D8A7A;
        border-radius: 10px;
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
