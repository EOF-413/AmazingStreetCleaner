import sys
import threading
import time

from pynput import keyboard
from PIL import ImageGrab
import numpy as np
from PyQt5.QtWidgets import QApplication

from config import load_config
from core.matcher import Matcher
from core.keyboard import press_key, release_all
from core.screen import get_region
from gui.main_window import MainWindow


class App:
    def __init__(self):
        self.matcher = Matcher()
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.listener = None
        self.gui = None

        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.daemon = True
        self.listener.start()

    def _on_press(self, key):
        if key == keyboard.Key.f9:
            self.toggle()
            return False
        return True

    def loop(self):
        while self.running:
            if not self.enabled:
                time.sleep(0.05)
                continue
            try:
                config = load_config()
                screenshot = ImageGrab.grab(bbox=self.region)
                gray = np.array(screenshot.convert('L'), dtype=np.uint8)

                key, score = self.matcher.process(gray)

                if key:
                    if self.gui:
                        self.gui.log_info(f"Удерживается {key} ({score}%)")
                    press_key(key, config["HOLD"])
                else:
                    press_key('e', 0.2)
                    if self.gui:
                        self.gui.log_warning(f"Нет совпадений ({score}%)")

                time.sleep(config["COOLDOWN"])
            except Exception as e:
                if self.gui:
                    self.gui.log_error(f"Ошибка: {e}")
                time.sleep(0.5)

    def start(self):
        if not self.enabled:
            self.enabled = True
            if self.gui:
                status = "GPU (CUDA)" if self.matcher.use_gpu else "CPU (без CUDA)"
                self.gui.log_info(f"Запущено на {status}")
                self.gui.update_status()
            if not self.loop_thread or not self.loop_thread.is_alive():
                self.loop_thread = threading.Thread(target=self.loop, daemon=True)
                self.loop_thread.start()

    def stop(self):
        self.enabled = False
        release_all()
        if self.gui:
            self.gui.log_info("Остановлено")
            self.gui.update_status()

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


if __name__ == '__main__':
    app = QApplication(sys.argv)

    auto_app = App()
    window = MainWindow(auto_app)
    auto_app.gui = window
    window.log_info("Нажмите F9 для старта")
    window.show()

    sys.exit(app.exec_())
