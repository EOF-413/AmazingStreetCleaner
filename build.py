import os
import sys
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_NAME = 'ASC'

print("=" * 50)
print("AmazingStreetCleaner - Сборка .exe")
print(f"Базовая папка: {BASE_DIR}")
print("=" * 50)

for folder in ['dist', 'build']:
    folder_path = os.path.join(BASE_DIR, folder)
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"[CLEAN] Удалена папка {folder_path}")

cmd = [
    sys.executable, '-m', 'PyInstaller',
    '--console',
    '--onedir',
    '--noupx',
    '--strip',
    '--exclude-module', 'matplotlib',
    '--exclude-module', 'scipy',
    f'--name={APP_NAME}',
    'main.py'
]

icon_path = os.path.join(BASE_DIR, 'icon.ico')
if os.path.exists(icon_path):
    cmd.insert(4, f'--icon={icon_path}')
    print("[OK] Иконка найдена")
else:
    print("[WARN] Иконка не найдена")

subprocess.run(cmd, cwd=BASE_DIR)

print("\n" + "=" * 50)

exe_path = os.path.join(BASE_DIR, 'dist', f'{APP_NAME}.exe')
src_templates = os.path.join(BASE_DIR, 'templates')
dst_templates = os.path.join(BASE_DIR, 'dist', APP_NAME, 'templates')
if os.path.exists(src_templates):
    if os.path.exists(dst_templates):
        shutil.rmtree(dst_templates)
    shutil.copytree(src_templates, dst_templates)
    print(f"[OK] Папка templates скопирована в {dst_templates}")
    files = os.listdir(dst_templates)
    print(f"   Содержит {len(files)} файлов: {', '.join(files)}")
else:
    print(f"[ERROR] Папка templates не найдена по пути {src_templates}")

src_config = os.path.join(BASE_DIR, 'config.json')
dst_config = os.path.join(BASE_DIR, 'dist', APP_NAME, 'config.json')
if os.path.exists(src_config):
    shutil.copy2(src_config, dst_config)
    print(f"[OK] config.json скопирован в {dst_config}")
else:
    print(f"[ERROR] config.json не найден по пути {src_config}")

dist_dir = os.path.join(BASE_DIR, 'dist', APP_NAME)
print("\n[CHECK] Содержимое dist/ASC:")
for item in os.listdir(dist_dir):
    item_path = os.path.join(dist_dir, item)
    if os.path.isdir(item_path):
        print(f"   📁 {item}/")
    else:
        print(f"   📄 {item}")

size = os.path.getsize(exe_path) / (1024 * 1024)
print("\n✅ Сборка завершена!")
print(f"📁 Размер .exe: {size:.2f} MB")
print(f"📁 {exe_path}")
input("\nНажмите Enter для выхода...")
