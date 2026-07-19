from time import sleep
from threading import Thread

import numpy as np
from PIL import ImageGrab
from pynput.keyboard import Listener, Key

from src.backend import Matcher, get_region, press_key, release_all
from src.config import load_config


class App:
    def __init__(self):
        self.matcher = Matcher()
        self.region = get_region()
        self.enabled = False
        self.running = True
        self.loop_thread = None
        self.gui = None
        self.listener = None

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
                        self.gui.log(f"Удерживается {key} ({score}%)", 'keyboard')
                    press_key(key, config["HOLD"])
                else:
                    press_key('E', 0.2)
                    if self.gui:
                        self.gui.log(f"Нет совпадений ({score}%)", 'nokey')

                sleep(config["COOLDOWN"])
            except Exception as e:
                if self.gui:
                    self.gui.log_error(f"Ошибка: {e}")
                sleep(0.5)

    def on_press(self, key):
        try:
            if key == Key.f9:
                if self.gui:
                    self.gui.toggle()
        except Exception:
            pass

    def start_listener(self):
        if self.listener is None or not self.listener.running:
            self.listener = Listener(on_press=self.on_press)
            self.listener.daemon = True
            self.listener.start()

    def start(self):
        if not self.enabled:
            self.enabled = True
            if self.gui:
                self.gui.log_info("Запущено")
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
        if self.listener and self.listener.running:
            self.listener.stop()
