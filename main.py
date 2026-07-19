import sys

from PyQt5.QtWidgets import QApplication

from src import App
from src.frontend import MainWindow


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        auto_app = App()
        window = MainWindow(auto_app)
        auto_app.gui = window
        window.log_info("Нажмите F9 для старта.")
        window.show()
        exit_code = app.exec_()
        auto_app.cleanup()
        sys.exit(exit_code)
    except Exception as e:
        print("Программа завершена с ошибкой:", e)
        input("Нажмите Enter для выхода...")
        sys.exit(1)
