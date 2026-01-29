# build_exe.py (ИСПРАВЛЕННЫЙ)
"""
Скрипт сборки текстового редактора в .exe файл для Windows
Использует PyInstaller для создания автономного исполняемого файла
"""
import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Сборка приложения в .exe файл"""
   
    print("=" * 70)
    print("🔨 СБОРКА ТЕКСТОВОГО РЕДАКТОРА В .EXE")
    print("=" * 70)
   
    # Проверяем наличие PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller найден")
    except ImportError:
        print("❌ PyInstaller не установлен")
        print(" Установка: pip install pyinstaller")
        return False
   
    # Путь к проекту
    project_dir = Path(__file__).parent / "."
    if not project_dir.exists():
        print(f"❌ Папка проекта не найдена: {project_dir}")
        return False
   
    print(f"📁 Проект: {project_dir}")
   
    # Переходим в папку проекта
    os.chdir(project_dir)
   
    # Параметры сборки
    main_py = project_dir / "main.py"
    if not main_py.exists():
        print(f"❌ Файл main.py не найден")
        return False
   
    output_dir = project_dir / "dist"
    build_dir = project_dir / "build"
   
    print("\n📦 Параметры сборки:")
    print(f" Входной файл: {main_py}")
    print(f" Выходная папка: {output_dir}")
   
    # Команда для PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Один файл без зависимостей
        "--windowed",  # Без консольного окна
        "--name", "TextEditor",  # Имя приложения
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtPrintSupport",
        "--hidden-import=app.core",
        "--hidden-import=app.features",
        "--hidden-import=app.ui",
        "--hidden-import=app.utils",
        str(main_py)
    ]
    
    # Добавляем иконку если она есть
    ico_path = Path("TextEditor.ico")
    if ico_path.exists():
        cmd.insert(cmd.index("--name"), f"--icon={ico_path}")
   
    print("\n🔨 Запуск PyInstaller...")
    print(f" Команда: {' '.join(cmd[:3])}...")
   
    try:
        result = subprocess.run(cmd, capture_output=False)
       
        if result.returncode == 0:
            exe_path = output_dir / "TextEditor.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print("\n" + "=" * 70)
                print(f"✅ СБОРКА УСПЕШНА!")
                print(f" Файл: {exe_path}")
                print(f" Размер: {size_mb:.2f} MB")
                print("=" * 70)
                return True
            else:
                print("❌ .exe файл не был создан")
                return False
        else:
            print("❌ Ошибка при сборке")
            return False
           
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def cleanup():
    """Удаление временных файлов сборки"""
    project_dir = Path(__file__).parent / "."
   
    cleanup_dirs = [
        project_dir / "build",
        project_dir / "__pycache__",
    ]
   
    cleanup_files = [
        project_dir / "TextEditor.spec",
    ]
   
    print("\n🧹 Очистка временных файлов...")
   
    for dir_path in cleanup_dirs:
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f" Удалена папка: {dir_path.name}")
   
    for file_path in cleanup_files:
        if file_path.exists():
            file_path.unlink()
            print(f" Удален файл: {file_path.name}")

def main():
    print("\n")
   
    # Проверяем Python версию
    if sys.version_info < (3, 8):
        print("❌ Требуется Python 3.8 или выше")
        print(f" Текущая версия: {sys.version_info.major}.{sys.version_info.minor}")
        return False
   
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
   
    # Проверяем PyQt6
    try:
        import PyQt6
        print("✅ PyQt6 установлен")
    except ImportError:
        print("❌ PyQt6 не установлен")
        print(" Установка: pip install PyQt6")
        return False
   
    # Выполняем сборку
    success = build_executable()
   
    # Очищаем временные файлы
    if success:
        cleanup()
   
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
