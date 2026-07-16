import time
import ctypes

user32 = ctypes.windll.user32

VK = {
    'a': 0x41, 'c': 0x43, 'd': 0x44, 'e': 0x45,
    'j': 0x4A, 'k': 0x4B, 'l': 0x4C, 'n': 0x4E,
    'q': 0x51, 'r': 0x52, 's': 0x53, 'w': 0x57,
    'alt': 0xA4, 'shift': 0xA0, 'ctrl': 0xA2
}

SC = {
    'a': 0x1E, 'c': 0x2E, 'd': 0x20, 'e': 0x12,
    'j': 0x24, 'k': 0x25, 'l': 0x26, 'n': 0x31,
    'q': 0x10, 'r': 0x13, 's': 0x1F, 'w': 0x11,
    'alt': 0x38, 'shift': 0x2A, 'ctrl': 0x1D
}

KEYEVENTF_KEYDOWN = 0x0000
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_EXTENDEDKEY = 0x0001


def press_key(key):
    try:
        if key not in VK:
            print(f"[WARNING] Неизвестная клавиша: {key}")
            return

        vk = VK[key]
        sc = SC.get(key, 0)

        if key in ['alt', 'shift', 'ctrl']:
            user32.keybd_event(vk, sc, KEYEVENTF_EXTENDEDKEY, 0)
        else:
            user32.keybd_event(vk, sc, KEYEVENTF_KEYDOWN, 0)

        time.sleep(1.5)

        if key in ['alt', 'shift', 'ctrl']:
            user32.keybd_event(vk, sc, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
        else:
            user32.keybd_event(vk, sc, KEYEVENTF_KEYUP, 0)

    except Exception as e:
        print(f"[ERROR] Ошибка при нажатии {key}: {e}")


def release_all():
    for key in VK:
        try:
            vk = VK[key]
            sc = SC.get(key, 0)

            if key in ['alt', 'shift', 'ctrl']:
                user32.keybd_event(vk, sc, KEYEVENTF_EXTENDEDKEY | KEYEVENTF_KEYUP, 0)
            else:
                user32.keybd_event(vk, sc, KEYEVENTF_KEYUP, 0)
        except:
            pass
