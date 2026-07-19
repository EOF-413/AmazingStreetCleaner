from datetime import datetime
import os
import sys

from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QTextCharFormat, QTextCursor, QIcon
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTextEdit, QGroupBox, QTabWidget
)

from src.config import load_config, VERSION
from src.frontend.settings import SettingsTab


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


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
            'info': self._create_format("#09ff00"),
            'warning': self._create_format('#ffaa00'),
            'error': self._create_format('#ff4444'),
            'default': self._create_format('#ffffff'),
            'settings': self._create_format("#7700ffff"),
            'keyboard': self._create_format("#8c45ff42"),
            'nokey': self._create_format("#ffce2e42"),
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
        self.config = load_config()

        self.setWindowTitle("AmazingStreetCleaner")
        self.resize(500, 550)
        self.setMinimumSize(300, 350)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        icon_path = resource_path('icon.ico')
        if os.path.exists(icon_path):
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
            QPushButton:disabled {
                background-color: #555555;
                color: #888888;
            }
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #1a1a1a;
            }
            QTabBar::tab {
                background-color: #2a2a2a;
                color: #ffffff;
                padding: 8px 20px;
                border: 1px solid #3d3d3d;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background-color: #3d3d3d;
            }
            QTabBar::tab:disabled {
                color: #666666;
            }
        """)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setSpacing(0)
        header_layout.setContentsMargins(0, 0, 0, 10)

        title = QLabel("AmazingStreetCleaner")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        header_layout.addWidget(title)

        version_label = QLabel(f"v{VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("font-size: 15px; color: #888888;")
        header_layout.addWidget(version_label)

        layout.addWidget(header_widget)

        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_main_tab(), "Главная")
        self.settings_tab = SettingsTab(self)
        self.tabs.addTab(self.settings_tab, "Настройки")
        layout.addWidget(self.tabs)

        self.start_btn = QPushButton("СТАРТ")
        self.start_btn.clicked.connect(self.toggle)
        self.start_btn.setFixedWidth(180)
        self.start_btn.setFixedHeight(40)

        bottom_layout = QVBoxLayout()
        bottom_layout.setSpacing(8)
        bottom_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        layout.addLayout(bottom_layout)

        self.append_text.connect(self._append_text_slot)

        self.timer = QTimer()
        self.timer.timeout.connect(self._update_config)
        self.timer.start(1000)

        self.app.start_listener()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F9:
            event.accept()
            return
        super().keyPressEvent(event)

    def _append_text_slot(self, text, tag):
        self.log_area.append_colored(text, tag)

    def _update_config(self):
        self.settings_tab.update_config()

    def _create_main_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        log_frame = QGroupBox("Лог")
        log_layout = QVBoxLayout()
        self.log_area = ColoredTextEdit()
        log_layout.addWidget(self.log_area)
        log_frame.setLayout(log_layout)
        layout.addWidget(log_frame)

        return tab

    def log(self, message, tag='default'):
        self.append_text.emit(message, tag)

    def log_info(self, message):
        self.log(message, 'info')

    def log_warning(self, message):
        self.log(message, 'warning')

    def log_error(self, message):
        self.log(message, 'error')

    def toggle(self):
        try:
            self.app.toggle()
            self.update_status()
            self._update_fields_state()
        except Exception:
            pass

    def update_status(self):
        if self.app.enabled:
            self.start_btn.setText("СТОП")
            self.start_btn.setObjectName("stop_btn")
            self.start_btn.setStyleSheet(self.start_btn.styleSheet())
        else:
            self.start_btn.setText("СТАРТ")
            self.start_btn.setObjectName("")
            self.start_btn.setStyleSheet(self.start_btn.styleSheet())

    def _update_fields_state(self):
        enabled = not self.app.enabled
        self.settings_tab.set_enabled(enabled)
        self.tabs.setTabEnabled(1, enabled)

    def closeEvent(self, event):
        try:
            self.app.cleanup()
        except Exception:
            pass
        event.accept()
