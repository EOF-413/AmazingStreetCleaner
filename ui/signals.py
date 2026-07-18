from PyQt5.QtCore import pyqtSignal, QObject


class Signals(QObject):
    update_overlay = pyqtSignal(str, str, int)
