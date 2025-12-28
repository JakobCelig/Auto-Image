from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QHBoxLayout,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QToolButton,
    QStackedWidget,
    QProgressBar,
)
from PyQt5.QtCore import Qt


class SettingsWidget(QWidget):
    """
    Left settings panel with image conversion controls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 12, 0, 0)
        layout.setSpacing(16)

        hint = QLabel("Tune crop detection and output shape.")
        hint.setObjectName("settingsHint")
        hint.setWordWrap(True)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(10)

        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 255)
        self.threshold_spin.setValue(100)
        self.threshold_spin.setSuffix(" alpha")

        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setDecimals(1)
        self.margin_spin.setRange(0.0, 100.0)
        self.margin_spin.setSingleStep(0.5)
        self.margin_spin.setValue(5.0)
        self.margin_spin.setSuffix(" %")

        aspect_row = QWidget()
        aspect_layout = QHBoxLayout(aspect_row)
        aspect_layout.setContentsMargins(0, 0, 0, 0)
        aspect_layout.setSpacing(6)

        self.aspect_w_spin = QSpinBox()
        self.aspect_w_spin.setRange(1, 9999)
        self.aspect_w_spin.setValue(4)

        self.aspect_h_spin = QSpinBox()
        self.aspect_h_spin.setRange(1, 9999)
        self.aspect_h_spin.setValue(3)

        ratio_label = QLabel(":")
        ratio_label.setAlignment(Qt.AlignCenter)
        ratio_label.setObjectName("ratioSeparator")

        aspect_layout.addWidget(self.aspect_w_spin)
        aspect_layout.addWidget(ratio_label)
        aspect_layout.addWidget(self.aspect_h_spin)

        form.addRow("Threshold", self.threshold_spin)
        form.addRow("Margin", self.margin_spin)
        form.addRow("Aspect ratio", aspect_row)

        output_row = QWidget()
        output_layout = QVBoxLayout(output_row)
        output_layout.setContentsMargins(0, 0, 0, 0)
        output_layout.setSpacing(8)

        self.output_path_label = QLabel("cropped")
        self.output_path_label.setWordWrap(True)
        self.output_path_label.setObjectName("outputPath")
        self.output_path_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )

        self.output_browse_button = QToolButton()
        self.output_browse_button.setText("Browse")
        self.output_browse_button.setCursor(Qt.PointingHandCursor)
        self.output_browse_button.setObjectName("outputBrowse")

        output_layout.addWidget(self.output_path_label)
        output_layout.addWidget(self.output_browse_button)

        form.addRow("Output folder", output_row)

        self.convert_button = QPushButton("Convert Images")
        self.convert_button.setCursor(Qt.PointingHandCursor)
        self.convert_button.setObjectName("convertButton")

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Converting... %p%")
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setObjectName("convertProgress")
        self.progress_bar.setFixedHeight(
            self.convert_button.sizeHint().height()
        )

        self.convert_stack = QStackedWidget()
        self.convert_stack.addWidget(self.convert_button)
        self.convert_stack.addWidget(self.progress_bar)

        self.remove_button = QPushButton("Remove All")
        self.remove_button.setCursor(Qt.PointingHandCursor)
        self.remove_button.setObjectName("removeButton")

        layout.addWidget(hint)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(self.convert_stack)
        layout.addWidget(self.remove_button)
