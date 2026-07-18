import os
import sys
import subprocess
import shutil

APP_NAME = 'ASC'

print("=" * 50)
print("AmazingStreetCleaner - Сборка .exe")
print("=" * 50)

for folder in ['dist', 'build']:
    if os.path.exists(folder):
        shutil.rmtree(folder)
        print(f"[CLEAN] Удалена папка {folder}")

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

if os.path.exists('icon.ico'):
    cmd.insert(4, '--icon=icon.ico')
    print("[OK] Иконка найдена")

subprocess.run(cmd)

print("\n" + "=" * 50)

exe_path = os.path.join('dist', f'{APP_NAME}.exe')
if os.path.exists(exe_path):
    src_templates = os.path.join(os.path.dirname(__file__), 'templates')
    dst_templates = os.path.join('dist', APP_NAME, 'templates')
    if os.path.exists(src_templates):
        if os.path.exists(dst_templates):
            shutil.rmtree(dst_templates)
        shutil.copytree(src_templates, dst_templates)
        print(f"[OK] Папка templates скопирована в {dst_templates}")
    else:
        print("[WARN] Папка templates не найдена в исходнике – скопируйте её вручную")

    size = os.path.getsize(exe_path) / (1024 * 1024)
    print("✅ Сборка завершена!")
    print(f"📁 Размер .exe: {size:.2f} MB")
    print(f"📁 {exe_path}")
    print("📁 Шаблоны лежат в dist/ASC/templates/")
else:
    print("❌ Сборка не удалась")
print("=" * 50)

input("\nНажмите Enter для выхода...")
