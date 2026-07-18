<<<<<<< HEAD
import threading
import time
import gc
import sys

from pynput import keyboard
from PIL import ImageGrab
import numpy as np
from PyQt5.QtWidgets import QApplication

from config import HOLD, COOLDOWN
from core.matcher import Matcher
from core.keyboard import press_key, release_all
from core.region import get_region
from gui.main_window import MainWindow

=======
import sys
import time
import threading
import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QFont, QColor, QPainter, QBrush, QPen
from pynput import keyboard
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
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d

class App:
    def __init__(self):
        self.matcher = Matcher()
<<<<<<< HEAD
=======
        if not self.matcher.templates:
            print("[WARNING] Нет шаблонов в папке templates/")
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.listener = None
<<<<<<< HEAD
        self.gui = None
        self.frame_count = 0

    def start_listener(self):
        def on_press(key):
            if key == keyboard.Key.f9:
                self.toggle()
                return False
=======
        
        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.signals = Signals()
        self.overlay = OverlayWindow(self.signals)
        self.overlay.show()
        
        self.start_listener()
        print("[READY] F9 - старт/стоп | ESC - выход")

    def start_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f9:
                    print("[DEBUG] F9 pressed")
                    self.toggle()
                    return False
                elif key == keyboard.Key.esc:
                    print("[DEBUG] ESC pressed")
                    self.cleanup()
                    return False
            except:
                pass
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
            return True

        if self.listener:
            self.listener.stop()
<<<<<<< HEAD
=======
        
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.daemon = True
        self.listener.start()

    def loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(0.05)
                continue
            try:
                screenshot = ImageGrab.grab(bbox=self.region)
<<<<<<< HEAD
                gray = np.array(screenshot.convert('L'), dtype=np.uint8)

                key, score = self.matcher.process(gray)

                if key:
                    press_key(key, HOLD)
                    if self.gui and self.frame_count % 10 == 0:
                        self.gui.log_info(f"Нажата {key} ({score}%)")
                else:
                    press_key('e', 0.2)
                    if self.gui and self.frame_count % 10 == 0:
                        self.gui.log_warning(f"Нет совпадений ({score}%)")

                self.frame_count += 1
                time.sleep(COOLDOWN)
            except Exception as e:
                if self.gui:
                    self.gui.log_error(f"Ошибка: {e}")
                time.sleep(0.5)
            finally:
                if self.frame_count % 100 == 0:
                    gc.collect()
=======
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
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d

    def start(self):
        if not self.enabled:
            self.enabled = True
<<<<<<< HEAD
            if self.gui:
                status = "GPU (CUDA)" if self.matcher.use_gpu else "CPU (без CUDA)"
                self.gui.log_info(f"Запущено на {status}")
                self.gui.update_status()
            if not self.loop_thread or not self.loop_thread.is_alive():
=======
            self.signals.update_overlay.emit("🟢 Активно", "#00FF00", 999999)
            if self.loop_thread is None or not self.loop_thread.is_alive():
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
                self.loop_thread = threading.Thread(target=self.loop, daemon=True)
                self.loop_thread.start()
            self.start_listener()

    def stop(self):
        self.enabled = False
        release_all()
<<<<<<< HEAD
        if self.gui:
            self.gui.log_info("Остановлено")
            self.gui.update_status()
=======
        self.signals.update_overlay.emit("⚫ Ожидание F9", "#888888", 999999)
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
        self.start_listener()

    def toggle(self):
        if self.enabled:
            self.stop()
        else:
            self.start()

    def cleanup(self):
        self.running = False
        self.enabled = False
        release_all()
        if self.listener:
            self.listener.stop()
<<<<<<< HEAD


if __name__ == '__main__':
    app = QApplication(sys.argv)

    auto_app = App()
    window = MainWindow(auto_app)
    auto_app.gui = window
    auto_app.start_listener()
    window.log_info("Нажмите F9 для старта")
    window.show()

    sys.exit(app.exec_())
=======
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
>>>>>>> 07e916b62679c3c5a84cdc9b692cbadac209434d
