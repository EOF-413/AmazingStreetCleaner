from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen


class OverlayWindow(QLabel):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
        self.setup_ui()
        self.setup_timer()
        self.connect_signals()

    def setup_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.font = QFont("Consolas", 12, QFont.Bold)
        self.setFont(self.font)

        self.setFixedSize(300, 70)
        self.move(10, 10)

        self.bg_color = QColor(0, 0, 0, 200)
        self.text_color = QColor(0, 255, 0)
        self.current_text = "⚫ Ожидание F9"

        self.setStyleSheet("background: transparent;")
        self.setText("")
        self.update()

    def setup_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset)

    def connect_signals(self):
        self.signals.update_overlay.connect(self.flash)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.bg_color))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 8, 8)

        painter.setPen(QPen(self.text_color))
        painter.setFont(self.font)
        painter.drawText(self.rect(), Qt.AlignCenter, self.current_text)

    def flash(self, text, color, duration):
        self.current_text = text
        self.text_color = QColor(color)
        self.bg_color = QColor(0, 0, 0, 200)
        self.update()
        self.show()

        if duration < 999999:
            self.timer.start(duration)

    def reset(self):
        self.timer.stop()
        self.bg_color = QColor(0, 0, 0, 200)
        self.text_color = QColor(0, 255, 0)

        if "Активно" in self.current_text:
            self.current_text = "🟢 Активно"
        else:
            self.current_text = "⚫ Ожидание F9"
            self.text_color = QColor(136, 136, 136)

        self.update()
