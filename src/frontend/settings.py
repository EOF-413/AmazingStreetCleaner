from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout,
    QLabel, QLineEdit, QPushButton, QGroupBox, QMessageBox
)

from src.config import load_config, save_config, DEFAULT_CONFIG


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.config = load_config()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        settings_frame = QGroupBox("Параметры")
        settings_layout = QGridLayout()
        settings_layout.setSpacing(10)
        settings_layout.setHorizontalSpacing(15)

        settings_layout.addWidget(QLabel("Время удержания:"), 0, 0)
        self.hold_edit = QLineEdit(str(self.config["HOLD"]))
        self.hold_edit.setFixedWidth(80)
        settings_layout.addWidget(self.hold_edit, 0, 1)

        settings_layout.addWidget(QLabel("Задержка:"), 1, 0)
        self.cooldown_edit = QLineEdit(str(self.config["COOLDOWN"]))
        self.cooldown_edit.setFixedWidth(80)
        settings_layout.addWidget(self.cooldown_edit, 1, 1)

        settings_layout.addWidget(QLabel("Порог совпадения:"), 2, 0)
        self.min_match_edit = QLineEdit(str(self.config["MIN_MATCH"]))
        self.min_match_edit.setFixedWidth(80)
        settings_layout.addWidget(self.min_match_edit, 2, 1)

        settings_frame.setLayout(settings_layout)
        layout.addWidget(settings_frame)

        reset_btn = QPushButton("Сбросить настройки")
        reset_btn.setFixedWidth(250)
        reset_btn.setFixedHeight(40)
        reset_btn.clicked.connect(self._reset_settings)
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12pt;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
            QPushButton:pressed {
                background-color: #bd2130;
            }
            QPushButton:disabled {
                background-color: #6c757d;
                color: #adb5bd;
            }
        """)

        layout.addWidget(reset_btn, alignment=Qt.AlignCenter)
        layout.addStretch()

    def _reset_settings(self):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Подтверждение")
        msg_box.setText("Сбросить все настройки к значениям по умолчанию?")
        msg_box.setInformativeText("Это действие нельзя отменить.")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)

        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #f0f0f0;
            }
            QLabel {
                color: #000000;
                background-color: #f0f0f0;
            }
            QPushButton {
                color: #000000;
                background-color: #e0e0e0;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #c0c0c0;
            }
        """)

        for button in msg_box.buttons():
            if msg_box.buttonRole(button) == QMessageBox.YesRole:
                button.setText("Да")
            elif msg_box.buttonRole(button) == QMessageBox.NoRole:
                button.setText("Нет")

        reply = msg_box.exec_()

        if reply == QMessageBox.Yes:
            self.config.update(DEFAULT_CONFIG)
            save_config(self.config)

            self.hold_edit.setText(str(self.config["HOLD"]))
            self.cooldown_edit.setText(str(self.config["COOLDOWN"]))
            self.min_match_edit.setText(str(self.config["MIN_MATCH"]))

            if self.parent_window:
                self.parent_window.log("Настройки сброшены к значениям по умолчанию", 'settings')

    def get_values(self):
        try:
            return {
                "HOLD": float(self.hold_edit.text()),
                "COOLDOWN": float(self.cooldown_edit.text()),
                "MIN_MATCH": float(self.min_match_edit.text())
            }
        except ValueError:
            return None

    def update_config(self):
        if self.parent_window and self.parent_window.app.enabled:
            return

        values = self.get_values()
        if values is None:
            return

        changed = False
        for key, val in values.items():
            if key in self.config and self.config[key] != val:
                if key == "HOLD" and 0.1 <= val <= 3.0:
                    self.config[key] = val
                    changed = True
                elif key == "COOLDOWN" and 0.1 <= val <= 2.0:
                    self.config[key] = val
                    changed = True
                elif key == "MIN_MATCH" and 0.1 <= val <= 0.9:
                    self.config[key] = val
                    changed = True

        if changed:
            save_config(self.config)

    def set_enabled(self, enabled):
        self.hold_edit.setEnabled(enabled)
        self.cooldown_edit.setEnabled(enabled)
        self.min_match_edit.setEnabled(enabled)
