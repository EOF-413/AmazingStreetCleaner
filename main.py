import sys
import time
import threading
import numpy as np
from PIL import ImageGrab

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

from pynput import keyboard

from config import KEY_MAP, COOLDOWN_AFTER_PRESS, CYCLE_DELAY
from core import Matcher, press_key, release_all, get_region
from ui.signals import Signals
from ui.overlay import OverlayWindow


class App:
    def __init__(self):
        self.matcher = Matcher()
        if not self.matcher.templates:
            sys.exit(1)

        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.stop_flag = threading.Event()
        self.toggle_flag = threading.Event()

        self.qt_app = QApplication.instance() or QApplication(sys.argv)
        self.signals = Signals()
        self.overlay = OverlayWindow(self.signals)
        self.overlay.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_flags)
        self.timer.start(50) 

        self.listener = None
        self.start_keyboard_listener()

        print("[READY] F9 - старт/стоп")
        print("[READY] ESC - выход")

    def start_keyboard_listener(self):
        def on_press(key):
            try:
                if key == keyboard.Key.f9:
                    print("[DEBUG] F9 нажат!")
                    self.toggle_flag.set()
                    return False
                elif key == keyboard.Key.esc:
                    print("[DEBUG] ESC нажат!")
                    self.cleanup()
                    return False
            except Exception as e:
                print(f"[ERROR] {e}")
            return True

        if self.listener and self.listener.running:
            self.listener.stop()
        
        self.listener = keyboard.Listener(on_press=on_press)
        self.listener.daemon = True
        self.listener.start()
        print("[LISTENER] Запущен")

    def check_flags(self):
        if self.toggle_flag.is_set():
            self.toggle_flag.clear()
            self.toggle()
            if not self.listener or not self.listener.running:
                self.start_keyboard_listener()

        if self.stop_flag.is_set():
            self.stop_flag.clear()
            self.running = False
            self.enabled = False
            release_all()
            if self.loop_thread and self.loop_thread.is_alive():
                self.loop_thread.join(timeout=1.0)
            self.qt_app.quit()

    def loop(self):
        """Основной цикл программы"""
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
            self.running = True
            self.signals.update_overlay.emit("🟢 Активно", "#00FF00", 999999)
            
            if self.loop_thread is None or not self.loop_thread.is_alive():
                self.loop_thread = threading.Thread(target=self.loop, daemon=True)
                self.loop_thread.start()
            
            print("[STATUS] Запущен")

    def stop(self):
        self.enabled = False
        release_all()
        self.signals.update_overlay.emit("⚫ Ожидание F9", "#888888", 999999)
        print("[STATUS] Остановлен")

    def toggle(self):
        if self.enabled:
            self.stop()
        else:
            self.start()

    def cleanup(self):
        print("[CLEANUP] Завершение работы...")
        self.stop_flag.set()  # Устанавливаем флаг остановки


if __name__ == '__main__':
    try:
        app = App()
        app.qt_app.exec_()
    except KeyboardInterrupt:
        app.cleanup()
    except Exception as e:
        print(f"[FATAL] {e}")
        app.cleanup()
