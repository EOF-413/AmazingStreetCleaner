import sys
from os import path
from datetime import datetime
from logging import exception

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QGridLayout
)

from config import load_config, save_config


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)


class ColoredTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: none;
                font-family: Consolas;
                font-size: 10pt;
            }
            QScrollBar:vertical {
                background: #2a2a2a;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #555555;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::handle:vertical:hover {
                background: #777777;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.formats = {
            'info': self._create_format('#00ff88'),
            'warning': self._create_format('#ffaa00'),
            'error': self._create_format('#ff4444'),
            'gpu': self._create_format('#4488ff'),
            'default': self._create_format('#ffffff'),
        }

    def _create_format(self, color):
        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))
        return fmt

    def append_colored(self, text, tag='default'):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        ts = datetime.now().strftime("%H:%M:%S")
        self.textCursor().insertText(f"[{ts}] ", self.formats['default'])
        self.textCursor().insertText(f"{text}\n", self.formats.get(tag, self.formats['default']))
        self.ensureCursorVisible()
        QApplication.processEvents()


class MainWindow(QMainWindow):
    append_text = pyqtSignal(str, str)

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.setWindowTitle("AmazingStreetCleaner")
        self.setMinimumSize(300, 450)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        icon_path = resource_path('icon.ico')
        if path.exists(icon_path):
            try:
                self.setWindowIcon(QIcon(icon_path))
            except Exception:
                pass

        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            QLabel {
                color: #ffffff;
            }
            QGroupBox {
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit {
                background-color: #3d3d3d;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: #ffffff;
                border: none;
                border-radius: 3px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #1a8ad4;
            }
            QPushButton:pressed {
                background-color: #0066b8;
            }
            QPushButton#stop_btn {
                background-color: #d32f2f;
            }
            QPushButton#stop_btn:hover {
                background-color: #e53935;
            }
            QPushButton#save_btn {
                background-color: #2e7d32;
            }
            QPushButton#save_btn:hover {
                background-color: #388e3c;
            }
        """)

        self.config = load_config()

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        title = QLabel("AmazingStreetCleaner")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff; padding: 10px;")
        layout.addWidget(title)

        gpu_frame = QGroupBox("Статус GPU")
        gpu_layout = QVBoxLayout()
        self.gpu_label = QLabel("Проверка GPU...")
        self.gpu_label.setAlignment(Qt.AlignCenter)
        self.gpu_label.setStyleSheet("color: #4488ff; font-weight: bold;")
        gpu_layout.addWidget(self.gpu_label)
        gpu_frame.setLayout(gpu_layout)
        layout.addWidget(gpu_frame)

        settings_frame = QGroupBox("Настройки")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(8)

        settings_layout.addWidget(QLabel("HOLD (сек):"), 0, 0)
        self.hold_edit = QLineEdit(str(self.config["HOLD"]))
        self.hold_edit.setFixedWidth(80)
        self.hold_edit.textChanged.connect(self._update_config)
        settings_layout.addWidget(self.hold_edit, 0, 1)

        settings_layout.addWidget(QLabel("COOLDOWN (сек):"), 1, 0)
        self.cooldown_edit = QLineEdit(str(self.config["COOLDOWN"]))
        self.cooldown_edit.setFixedWidth(80)
        self.cooldown_edit.textChanged.connect(self._update_config)
        settings_layout.addWidget(self.cooldown_edit, 1, 1)

        settings_layout.addWidget(QLabel("MIN DEF KEYS:"), 2, 0)
        self.min_def_edit = QLineEdit(str(self.config["MIN_DEF_KEYS"]))
        self.min_def_edit.setFixedWidth(80)
        self.min_def_edit.textChanged.connect(self._update_config)
        settings_layout.addWidget(self.min_def_edit, 2, 1)

        settings_layout.addWidget(QLabel("MIN DIG KEYS:"), 3, 0)
        self.min_dig_edit = QLineEdit(str(self.config["MIN_DIG_KEYS"]))
        self.min_dig_edit.setFixedWidth(80)
        self.min_dig_edit.textChanged.connect(self._update_config)
        settings_layout.addWidget(self.min_dig_edit, 3, 1)

        settings_frame.setLayout(settings_layout)
        layout.addWidget(settings_frame)

        log_frame = QGroupBox("Лог")
        log_layout = QVBoxLayout()
        self.log_area = ColoredTextEdit()
        log_layout.addWidget(self.log_area)
        log_frame.setLayout(log_layout)
        layout.addWidget(log_frame)

        bottom_frame = QWidget()
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setSpacing(8)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        self.start_btn = QPushButton("▶ СТАРТ")
        self.start_btn.clicked.connect(self.toggle)
        self.start_btn.setFixedWidth(180)
        bottom_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)

        layout.addWidget(bottom_frame)

        self.append_text.connect(self._append_text_slot)

        self.update_gpu_status()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gpu_status)
        self.timer.start(5000)

    def _append_text_slot(self, text, tag):
        self.log_area.append_colored(text, tag)

    def _update_config(self):
        changed = False
        try:
            val = float(self.hold_edit.text())
            if 0.1 <= val <= 3.0:
                self.config["HOLD"] = val
                changed = True
        except Exception as e:
            exception("Ошибка обновления HOLD:", e)
        try:
            val = float(self.cooldown_edit.text())
            if 0.1 <= val <= 2.0:
                self.config["COOLDOWN"] = val
                changed = True
        except Exception as e:
            exception("Ошибка обновления COOLDOWN:", e)
        try:
            val = float(self.min_def_edit.text())
            if 0.1 <= val <= 0.9:
                self.config["MIN_DEF_KEYS"] = val
                changed = True
        except Exception as e:
            exception("Ошибка обновления MIN_DEF_KEYS:", e)
        try:
            val = float(self.min_dig_edit.text())
            if 0.1 <= val <= 0.9:
                self.config["MIN_DIG_KEYS"] = val
                changed = True
        except Exception as e:
            exception("Ошибка обновления MIN_DIG_KEYS:", e)
        if changed:
            save_config(self.config)

    def update_gpu_status(self):
        try:
            status = self.app.matcher.get_gpu_status()
            self.gpu_label.setText(status)
        except Exception as e:
            exception("Ошибка обновления статуса GPU:", e)
            self.gpu_label.setText("❌ Ошибка проверки GPU")

    def log(self, message, tag='default'):
        self.append_text.emit(message, tag)

    def log_info(self, message):
        self.log(message, 'info')

    def log_warning(self, message):
        self.log(message, 'warning')

    def log_error(self, message):
        self.log(message, 'error')

    def log_gpu(self, message):
        self.log(message, 'gpu')
        self.gpu_label.setText(message)

    def toggle(self):
        try:
            self.app.toggle()
            self.update_status()
        except Exception as e:
            exception("Ошибка при переключении:", e)

    def update_status(self):
        if self.app.enabled:
            self.start_btn.setText("⏹ СТОП")
            self.start_btn.setObjectName("stop_btn")
            self.start_btn.setStyleSheet(self.start_btn.styleSheet())
        else:
            self.start_btn.setText("▶ СТАРТ")
            self.start_btn.setObjectName("")
            self.start_btn.setStyleSheet(self.start_btn.styleSheet())

    def closeEvent(self, event):
        try:
            self.app.cleanup()
        except Exception as e:
            exception("Ошибка при очистке:", e)
        event.accept()
