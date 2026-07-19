from time import sleep
from pynput.keyboard import Key, Controller

keyboard = Controller()

VK_TO_PYNPUT = {
    'A': 'a',
    'C': 'c',
    'D': 'd',
    'E': 'e',
    'J': 'j',
    'K': 'k',
    'L': 'l',
    'N': 'n',
    'Q': 'q',
    'R': 'r',
    'S': 's',
    'W': 'w',
    'SHIFT': Key.shift,
    'CTRL': Key.ctrl,
    'ALT': Key.alt
}

MODIFIERS = ['SHIFT', 'CTRL', 'ALT']


def press_key(key, hold):
    try:
        if key in MODIFIERS:
            keyboard.press(VK_TO_PYNPUT[key])
            sleep(hold)
            keyboard.release(VK_TO_PYNPUT[key])
        else:
            keyboard.press(key.lower())
            sleep(hold)
            keyboard.release(key.lower())
    except Exception:
        pass


def release_all():
    try:
        for key in MODIFIERS:
            keyboard.release(VK_TO_PYNPUT[key])
        for key in ['A', 'C', 'D', 'E', 'J', 'K', 'L', 'N', 'Q', 'R', 'S', 'W']:
            keyboard.release(key.lower())
    except Exception:
        pass
