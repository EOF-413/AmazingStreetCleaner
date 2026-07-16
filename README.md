# KeyPressAuto

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/KeyPressAuto)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.7+-yellow.svg)](https://www.python.org/)

Автоматическое нажатие клавиш на основе распознавания шаблонов на экране.

## 📋 Описание

KeyPressAuto - это программа для автоматизации нажатий клавиш в играх и приложениях. Она анализирует область экрана, распознает шаблоны и эмулирует нажатие соответствующих клавиш.

### Возможности
- 🎯 Распознавание шаблонов на экране с помощью OpenCV
- ⌨️ Автоматическое нажатие клавиш через Win32 API
- 🎨 Полупрозрачный оверлей с информацией о состоянии
- ⚡ Высокая скорость работы (задержка ~1мс)
- 🔧 Гибкие настройки через config.py
- 🖥️ Поддержка модификаторов (Ctrl, Shift, Alt)

## 📦 Установка

### Из исходников

```bash
# Клонирование репозитория
git clone https://github.com/EOF-413/AmazingAutoHotkeys
cd KeyPressAuto

# Создание виртуального окружения
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
# source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
