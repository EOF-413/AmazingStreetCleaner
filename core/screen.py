import ctypes
from config import X1_RATIO, Y1_RATIO, X2_RATIO, Y2_RATIO


def get_region():
    user32 = ctypes.windll.user32
    w = user32.GetSystemMetrics(0)
    h = user32.GetSystemMetrics(1)
    return (
        int(w * X1_RATIO),
        int(h * Y1_RATIO),
        int(w * X2_RATIO),
        int(h * Y2_RATIO)
    )
