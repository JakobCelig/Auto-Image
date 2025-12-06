import sys
from PyQt5.QtWidgets import QApplication
import qdarkstyle

from widgets.main_widget import MainWidget
from controllers.main_controller import MainController


def main():
    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    widget = MainWidget()
    controller = MainController(widget)

    widget.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
