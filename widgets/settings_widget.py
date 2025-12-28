from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QHBoxLayout,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
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
        self.aspect_w_spin.setRange(1, 32)
        self.aspect_w_spin.setValue(4)

        self.aspect_h_spin = QSpinBox()
        self.aspect_h_spin.setRange(1, 32)
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

        self.convert_button = QPushButton("Convert Images")
        self.convert_button.setCursor(Qt.PointingHandCursor)
        self.convert_button.setObjectName("convertButton")

        layout.addWidget(hint)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(self.convert_button)
