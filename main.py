import sys
import time
import threading
import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
import keyboard
from config import KEY_MAP, HOLD_TIME, CYCLE_DELAY, COOLDOWN_AFTER_PRESS
from core import Matcher, press_key, release_all, get_region

class Signals(QObject):
    update_overlay = pyqtSignal(str, str, int)

class OverlayWindow(QLabel):
    def __init__(self, signals):
        super().__init__()
        self.signals = signals
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
        self.timer = QTimer()
        self.timer.timeout.connect(self.reset)
        self.signals.update_overlay.connect(self.flash)
        self.update()

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

class App:
    def __init__(self):
        self.matcher = Matcher()
        if not self.matcher.templates:
            print("[WARNING] Нет шаблонов в папке templates/")
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.signals = Signals()
        self.overlay = OverlayWindow(self.signals)
        self.overlay.show()
        keyboard.add_hotkey('f9', self.toggle)
        keyboard.add_hotkey('esc', self.cleanup)
        print("[READY] F9 - старт/стоп | ESC - выход")

    def loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(0.05)
                continue
            try:
                screenshot = ImageGrab.grab(bbox=self.region)
                gray = np.array(screenshot.convert('L'))
                name, score = self.matcher.match(gray)
                if name:
                    key = KEY_MAP[name]
                    self.signals.update_overlay.emit(f"🟢 {name} → {key}", "#00FF00", 1500)
                    press_key(key)
                else:
                    self.signals.update_overlay.emit(f"🔴 ? → e  ({score:.2f})", "#FF4444", 800)
                    press_key('e')
                time.sleep(COOLDOWN_AFTER_PRESS)
                time.sleep(CYCLE_DELAY)
            except Exception as e:
                print(f"[ERROR] {e}")
                time.sleep(0.5)

    def start(self):
        if not self.enabled:
            self.enabled = True
            self.signals.update_overlay.emit("🟢 Активно", "#00FF00", 999999)
            if self.loop_thread is None or not self.loop_thread.is_alive():
                self.loop_thread = threading.Thread(target=self.loop, daemon=True)
                self.loop_thread.start()

    def stop(self):
        self.enabled = False
        release_all()
        self.signals.update_overlay.emit("⚫ Ожидание F9", "#888888", 999999)

    def toggle(self):
        if self.enabled:
            self.stop()
        else:
            self.start()

    def cleanup(self):
        self.running = False
        self.enabled = False
        release_all()
        if hasattr(self, 'qt_app'):
            self.qt_app.quit()
        sys.exit(0)

if __name__ == '__main__':
    try:
        app = App()
        app.qt_app.exec_()
    except KeyboardInterrupt:
        app.cleanup()
    except Exception as e:
        print(f"[FATAL] {e}")
        sys.exit(1)
