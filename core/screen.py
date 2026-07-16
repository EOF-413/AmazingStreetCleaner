import tkinter as tk
from config import X1_RATIO, Y1_RATIO, X2_RATIO, Y2_RATIO


def get_region():
    r = tk.Tk()
    w = r.winfo_screenwidth()
    h = r.winfo_screenheight()
    r.destroy()

    return (
        int(w * X1_RATIO),
        int(h * Y1_RATIO),
        int(w * X2_RATIO),
        int(h * Y2_RATIO)
    )
