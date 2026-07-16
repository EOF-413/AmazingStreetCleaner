import os
import sys
import shutil
import subprocess

APP_NAME = "KeyPressAuto"

def clean_build():
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)

def build_exe():
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", APP_NAME,
        "--add-data", "templates;templates",
        "--hidden-import", "PyQt5",
        "--hidden-import", "PyQt5.QtCore",
        "--hidden-import", "PyQt5.QtWidgets",
        "--hidden-import", "PyQt5.QtGui",
        "--hidden-import", "cv2",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.ImageGrab",
        "--hidden-import", "keyboard",
        "--hidden-import", "pyautogui",
        "--hidden-import", "tkinter",
        "--hidden-import", "ctypes",
        "main.py"
    ]
    subprocess.check_call(cmd)

def copy_files():
    if os.path.exists("config.py"):
        shutil.copy2("config.py", os.path.join("dist", "config.py"))
    
    bat_content = '''@echo off
title KeyPressAuto
echo ========================================
echo  KeyPressAuto
echo ========================================
echo.
echo Запуск программы...
start "" "KeyPressAuto.exe"
echo.
echo Программа запущена!
echo Нажмите F9 для старта/остановки
echo Нажмите ESC для выхода
pause
'''
    with open(os.path.join("dist", "Запуск KeyPressAuto.bat"), "w", encoding='utf-8') as f:
        f.write(bat_content)

if __name__ == "__main__":
    print("Сборка...")
    clean_build()
    build_exe()
    copy_files()
    print("Готово! .exe в папке dist/")
