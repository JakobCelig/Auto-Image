from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QHBoxLayout,
    QAbstractSpinBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QToolButton,
    QStackedWidget,
    QProgressBar,
    QSizePolicy,
)
from PyQt5.QtCore import Qt
from widgets.ui_scaling import scaled


class SettingsWidget(QWidget):
    """
    Left settings panel with image conversion controls.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("settingsWidget")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, scaled(12), 0, 0)
        layout.setSpacing(scaled(16))

        hint = QLabel("Tune crop detection and output shape.")
        hint.setObjectName("settingsHint")
        hint.setWordWrap(True)
        hint.setVisible(True)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignLeft)
        form.setFormAlignment(Qt.AlignTop)
        form.setHorizontalSpacing(scaled(12))
        form.setVerticalSpacing(scaled(10))
        form.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

        self.threshold_spin = QSpinBox()
        self.threshold_spin.setRange(0, 255)
        self.threshold_spin.setValue(100)
        self.threshold_spin.setSuffix(" alpha")
        self.threshold_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.threshold_spin.setFixedHeight(scaled(36))
        self._bind_spin_finish(self.threshold_spin)

        self.margin_spin = QDoubleSpinBox()
        self.margin_spin.setDecimals(1)
        self.margin_spin.setRange(0.0, 100.0)
        self.margin_spin.setSingleStep(0.5)
        self.margin_spin.setValue(5.0)
        self.margin_spin.setSuffix(" %")
        self.margin_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.margin_spin.setFixedHeight(scaled(36))
        self._bind_spin_finish(self.margin_spin)

        aspect_row = QWidget()
        aspect_row.setObjectName("aspectRow")
        aspect_row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        aspect_layout = QHBoxLayout(aspect_row)
        aspect_layout.setContentsMargins(0, 0, 0, 0)
        aspect_layout.setSpacing(scaled(6))

        self.aspect_w_spin = QSpinBox()
        self.aspect_w_spin.setRange(1, 9999)
        self.aspect_w_spin.setValue(4)
        self.aspect_w_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.aspect_w_spin.setFixedHeight(scaled(36))
        self.aspect_w_spin.setAlignment(Qt.AlignCenter)
        self._bind_spin_finish(self.aspect_w_spin)

        self.aspect_h_spin = QSpinBox()
        self.aspect_h_spin.setRange(1, 9999)
        self.aspect_h_spin.setValue(3)
        self.aspect_h_spin.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.aspect_h_spin.setFixedHeight(scaled(36))
        self.aspect_h_spin.setAlignment(Qt.AlignCenter)
        self._bind_spin_finish(self.aspect_h_spin)

        ratio_label = QLabel(":")
        ratio_label.setAlignment(Qt.AlignCenter)
        ratio_label.setObjectName("ratioSeparator")
        ratio_label.setFixedWidth(scaled(10))
        ratio_label.setFixedHeight(scaled(36))

        digits_width = self.aspect_w_spin.fontMetrics().horizontalAdvance("9999")
        spin_width = digits_width + scaled(44)
        for spin in (self.aspect_w_spin, self.aspect_h_spin):
            spin.setMinimumWidth(spin_width)
            spin.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        aspect_row.setFixedHeight(scaled(36))

        aspect_layout.addWidget(self.aspect_w_spin, stretch=1)
        aspect_layout.addWidget(ratio_label, stretch=0)
        aspect_layout.addWidget(self.aspect_h_spin, stretch=1)

        aspect_min_width = (
            self.aspect_w_spin.minimumWidth()
            + self.aspect_h_spin.minimumWidth()
            + ratio_label.sizeHint().width()
            + (aspect_layout.spacing() * 2)
        )

        form.addRow("Threshold", self.threshold_spin)
        form.addRow("Margin", self.margin_spin)
        form.addRow("Aspect ratio", aspect_row)

        output_label = QLabel("Output path")
        output_label.setObjectName("outputLabel")

        self.output_browse_button = QToolButton()
        self.output_browse_button.setText("Browse")
        self.output_browse_button.setCursor(Qt.PointingHandCursor)
        self.output_browse_button.setObjectName("outputBrowse")
        self.output_browse_button.setFixedHeight(scaled(36))
        self.output_browse_button.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        self.output_path_label = QLabel("cropped")
        self.output_path_label.setWordWrap(True)
        self.output_path_label.setObjectName("outputPath")
        self.output_path_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        self.output_path_label.setFixedHeight(scaled(36))
        self.output_path_label.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed,
        )

        form.addRow(output_label, self.output_browse_button)
        form.addRow(self.output_path_label)

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
        self.convert_stack.setObjectName("convertStack")
        self.convert_stack.addWidget(self.convert_button)
        self.convert_stack.addWidget(self.progress_bar)

        self.remove_button = QPushButton("Close All")
        self.remove_button.setCursor(Qt.PointingHandCursor)
        self.remove_button.setObjectName("removeButton")

        layout.addWidget(hint)
        layout.addLayout(form)
        layout.addStretch(1)
        layout.addWidget(self.convert_stack)
        layout.addWidget(self.remove_button)

        label_widgets = [
            form.labelForField(self.threshold_spin),
            form.labelForField(self.margin_spin),
            form.labelForField(aspect_row),
            form.labelForField(self.output_browse_button),
        ]
        label_width = max(
            (label.sizeHint().width() for label in label_widgets if label),
            default=0,
        )
        min_field_width = max(
            self.threshold_spin.minimumSizeHint().width(),
            self.margin_spin.minimumSizeHint().width(),
            aspect_min_width,
            self.output_browse_button.minimumSizeHint().width(),
        )
        min_width = label_width + form.horizontalSpacing() + min_field_width
        min_width += layout.contentsMargins().left()
        min_width += layout.contentsMargins().right()
        self.setMinimumWidth(min_width + scaled(6))

    def _bind_spin_finish(self, spin):
        spin.editingFinished.connect(lambda: self._finalize_spin(spin))

    @staticmethod
    def _finalize_spin(spin):
        line_edit = spin.lineEdit()
        if line_edit:
            line_edit.deselect()
        spin.clearFocus()

    def clear_focus_state(self):
        for spin in (
            self.threshold_spin,
            self.margin_spin,
            self.aspect_w_spin,
            self.aspect_h_spin,
        ):
            line_edit = spin.lineEdit()
            if line_edit:
                line_edit.deselect()
            spin.clearFocus()
