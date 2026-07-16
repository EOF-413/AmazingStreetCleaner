import sys
import subprocess

def install_requirements():
    print("Установка зависимостей...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "opencv-python", "numpy", "Pillow", "PyQt5", 
                          "keyboard", "pyautogui", "pyinstaller"])

def build():
    print("Сборка .exe...")

    try:
        import PyInstaller
    except ImportError:
        install_requirements()

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "KeyPressAuto",
        "--add-data", "config.py;.",
        "--add-data", "templates;templates",
        "--hidden-import", "PyQt5",
        "--hidden-import", "cv2",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "keyboard",
        "--hidden-import", "pyautogui",
        "main.py"
    ]

    subprocess.check_call(cmd)
    print("Готово! .exe файл в папке dist/")

if __name__ == "__main__":
    build()