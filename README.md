# 🚀 Amazing Street Cleaner

<div align="center">

[![Version](https://img.shields.io/badge/version-3.2.0-blue.svg)](https://github.com/EOF-413/AmazingStreetCleaner)
[![Python](https://img.shields.io/badge/python-3.11.0-yellow.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Windows](https://img.shields.io/badge/platform-Windows-blue.svg)](https://www.microsoft.com/windows)

**Автоматическое нажатие клавиш по шаблонам на экране**

</div>

---

## 📋 Описание

Amazing Street Cleaner - это программа для автоматического нажатия клавиш на работе уборщика улиц, проекта AMAZING ONLINE.

### ✨ Возможности

- 🖥️ **Глобальный хоткей** - F9 для старта/остановки.
- 🎨 **Современный интерфейс** - тёмная тема на PyQt5.
- 💾 **Сохранение настроек** - конфиг хранится в `%AppData%/EOF-413/ASC`.
- 🔧 **Гибкие настройки** - все параметры можно менять в реальном времени.
- 🎯 **Распознавание шаблонов** - использует OpenCV для поиска изображений на экране.

---

## 📦 Установка

### Способ 1: Установка из установщика (рекомендуется)

1. Скачайте установщик `ASC.exe`
2. Запустите установщик и следуйте инструкциям
3. Запустите программу через ярлык на рабочем столе или в меню Пуск

### Способ 2: Запуск из исходников

```bash
# Клонирование репозитория
git clone https://github.com/EOF-413/AmazingStreetCleaner.git

# Вход в каталог
cd AmazingStreetCleaner

# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск программы
python main.py
