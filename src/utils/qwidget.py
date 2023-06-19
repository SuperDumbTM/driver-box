from PyQt5 import QtWidgets


def is_widget_enabled(widget: QtWidgets.QWidget):
    if (type(widget) is QtWidgets.QCheckBox
            or type(widget) is QtWidgets.QRadioButton):
        return widget.isCheckable() and widget.isEnabled()
    else:
        return widget.isEnabled()
