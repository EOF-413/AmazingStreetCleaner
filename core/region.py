import tkinter as tk

from config import X1_RATIO, Y1_RATIO, X2_RATIO, Y2_RATIO


def get_region():
    root = tk.Tk()
    w = root.winfo_screenwidth()
    h = root.winfo_screenheight()
    root.destroy()

    return (
        int(w * X1_RATIO),
        int(h * Y1_RATIO),
        int(w * X2_RATIO),
        int(h * Y2_RATIO)
    )
