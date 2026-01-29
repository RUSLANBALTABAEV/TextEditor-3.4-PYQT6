# app/utils/icon_manager.py (ИСПРАВЛЕННЫЙ)
"""
Менеджер иконок для TextEditor
Загружает и управляет иконками для UI элементов
"""
import sys
import os
from pathlib import Path
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication

def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу, работает в dev и в PyInstaller."""
    try:
        # PyInstaller создаёт временную папку _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class IconManager:
    """Управление иконками приложения"""
   
    def __init__(self):
        # Папка с иконками с использованием resource_path
        icons_dir = Path(resource_path("app/icons"))
        self.icons_dir = icons_dir
       
        # Кэш иконок
        self.icons_cache = {}
   
    def get_icon(self, icon_name: str, size: int = 24) -> QIcon:
        """Получить иконку по имени"""
       
        # Проверяем кэш
        cache_key = f"{icon_name}_{size}"
        if cache_key in self.icons_cache:
            return self.icons_cache[cache_key]
       
        # Ищем иконку в папке
        icon_path = self.icons_dir / f"{icon_name}.png"
        if not icon_path.exists():
            # Ищем альтернативную версию
            icon_path = self.icons_dir / f"{icon_name}_flat.png"
       
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            if not pixmap.isNull():
                # Масштабируем если нужно
                if pixmap.width() != size:
                    pixmap = pixmap.scaledToWidth(size)
                icon = QIcon(pixmap)
                self.icons_cache[cache_key] = icon
                return icon
       
        # Возвращаем пустую иконку если файл не найден
        return QIcon()
   
    # Предопределенные иконки
   
    def file_new(self, size: int = 24) -> QIcon:
        """Иконка 'Новый файл'"""
        return self.get_icon("file_new_flat", size)
   
    def file_open(self, size: int = 24) -> QIcon:
        """Иконка 'Открыть файл'"""
        return self.get_icon("file_open_flat", size)
   
    def file_save(self, size: int = 24) -> QIcon:
        """Иконка 'Сохранить'"""
        return self.get_icon("file_save_flat", size)
   
    def file_print(self, size: int = 24) -> QIcon:
        """Иконка 'Печать'"""
        return self.get_icon("file_print_flat", size)
   
    def edit_undo(self, size: int = 24) -> QIcon:
        """Иконка 'Отменить'"""
        return self.get_icon("edit_undo", size)
   
    def edit_redo(self, size: int = 24) -> QIcon:
        """Иконка 'Повторить'"""
        return self.get_icon("edit_redo", size)
   
    def edit_cut(self, size: int = 24) -> QIcon:
        """Иконка 'Вырезать'"""
        return self.get_icon("edit_cut", size)
   
    def edit_copy(self, size: int = 24) -> QIcon:
        """Иконка 'Копировать'"""
        return self.get_icon("edit_copy", size)
   
    def edit_paste(self, size: int = 24) -> QIcon:
        """Иконка 'Вставить'"""
        return self.get_icon("edit_paste", size)
   
    def search_find(self, size: int = 24) -> QIcon:
        """Иконка 'Найти'"""
        return self.get_icon("search_find_flat", size)
   
    def search_replace(self, size: int = 24) -> QIcon:
        """Иконка 'Заменить'"""
        return self.get_icon("search_replace_flat", size)
   
    def view_zoom_in(self, size: int = 24) -> QIcon:
        """Иконка 'Масштаб+'"""
        return self.get_icon("view_zoom_in_flat", size)
   
    def view_zoom_out(self, size: int = 24) -> QIcon:
        """Иконка 'Масштаб-'"""
        return self.get_icon("view_zoom_out_flat", size)
   
    def tool_settings(self, size: int = 24) -> QIcon:
        """Иконка 'Настройки'"""
        return self.get_icon("tool_settings_flat", size)
   
    def tool_help(self, size: int = 24) -> QIcon:
        """Иконка 'Справка'"""
        return self.get_icon("tool_help_flat", size)
   
    def app_icon(self, size: int = 256) -> QIcon:
        """Главная иконка приложения"""
        return self.get_icon("app_main", size)
# Глобальный экземпляр менеджера иконок
_icon_manager = None
def get_icon_manager() -> IconManager:
    """Получить глобальный менеджер иконок"""
    global _icon_manager
    if _icon_manager is None:
        _icon_manager = IconManager()
    return _icon_manager
