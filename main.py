import sys
import keyboard
from time import sleep
from threading import Thread
from logging import basicConfig, ERROR, exception
from os import path

import numpy as np
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication

from config import load_config
from core.keyboard import press_key, release_all
from core.matcher import Matcher
from core.screen import get_region
from gui.main_window import MainWindow


def setup_logging():
    if getattr(sys, 'frozen', False):
        log_dir = path.dirname(sys.executable)
    else:
        log_dir = path.dirname(path.abspath(__file__))
    log_file = path.join(log_dir, 'log.txt')
    basicConfig(
        filename=log_file,
        level=ERROR,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )


class App:
    def __init__(self):
        self.matcher = Matcher()
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.gui = None

        # Регистрируем глобальную горячую клавишу F9
        keyboard.add_hotkey('f9', self.toggle, suppress=True)

    def loop(self):
        while self.running:
            if not self.enabled:
                sleep(0.05)
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

                sleep(config["COOLDOWN"])
            except Exception as e:
                exception("Ошибка в основном цикле:", e)
                if self.gui:
                    self.gui.log_error(f"Ошибка: {e}")
                sleep(0.5)

    def start(self):
        if not self.enabled:
            self.enabled = True
            if self.gui:
                status = "GPU (CUDA)" if self.matcher.use_gpu else "CPU (без CUDA)"
                self.gui.log_info(f"Запущено на {status}")
                self.gui.update_status()
            if not self.loop_thread or not self.loop_thread.is_alive():
                self.loop_thread = Thread(target=self.loop, daemon=True)
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
        keyboard.unhook_all()      # отключаем все горячие клавиши


if __name__ == '__main__':
    setup_logging()
    try:
        app = QApplication(sys.argv)
        auto_app = App()
        window = MainWindow(auto_app)
        auto_app.gui = window
        window.log_info("Нажмите F9 для старта (требуются права администратора)")
        window.show()
        exit_code = app.exec_()

        auto_app.cleanup()
        sys.exit(exit_code)
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("\nПрограмма завершена с ошибкой:", e)
        input("Нажмите Enter для выхода...")
        sys.exit(1)
