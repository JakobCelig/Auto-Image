from PyQt5.QtWidgets import QApplication


def ui_scale() -> float:
    app = QApplication.instance()
    if not app:
        return 1.0
    scale = app.property("ui_scale")
    try:
        return float(scale)
    except (TypeError, ValueError):
        return 1.0


def scaled(value: float) -> int:
    return int(round(value * ui_scale()))
