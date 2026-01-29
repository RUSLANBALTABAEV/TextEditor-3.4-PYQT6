# app/utils/icon_manager.py (ИСПРАВЛЕННЫЙ)
"""
Менеджер иконок для TextEditor - работает без файлов иконок
Использует встроенные стили и символы Qt
"""
from PyQt6.QtGui import QIcon, QPixmap, QColor, QPainter
from PyQt6.QtWidgets import QStyle, QApplication
from PyQt6.QtCore import QSize, Qt

class IconManager:
    """Управление иконками приложения - встроенные иконки без файлов"""
   
    def __init__(self):
        self.icons_cache = {}
   
    def _get_system_icon(self, icon_name: str) -> QIcon:
        """Получить иконку из системного стиля Qt"""
        app = QApplication.instance()
        if not app:
            return QIcon()
       
        style = app.style()
        
        # Соответствие имен к стандартным иконкам Qt
        icon_map = {
            'file_new': QStyle.StandardPixmap.SP_FileDialogNewFolder,
            'file_open': QStyle.StandardPixmap.SP_DirOpenIcon,
            'file_save': QStyle.StandardPixmap.SP_DialogYesButton,
            'file_print': QStyle.StandardPixmap.SP_FileDialogDetailedView,
            'edit_undo': QStyle.StandardPixmap.SP_ArrowLeft,
            'edit_redo': QStyle.StandardPixmap.SP_ArrowRight,
            'edit_cut': QStyle.StandardPixmap.SP_FileDialogDetailedView,
            'edit_copy': QStyle.StandardPixmap.SP_FileDialogListView,
            'edit_paste': QStyle.StandardPixmap.SP_DirIcon,
            'search_find': QStyle.StandardPixmap.SP_FileDialogDetailedView,
            'search_replace': QStyle.StandardPixmap.SP_FileDialogDetailedView,
            'view_zoom_in': QStyle.StandardPixmap.SP_ArrowUp,
            'view_zoom_out': QStyle.StandardPixmap.SP_ArrowDown,
            'tool_settings': QStyle.StandardPixmap.SP_FileDialogDetailedView,
            'tool_help': QStyle.StandardPixmap.SP_FileDialogInfoView,
        }
        
        if icon_name in icon_map:
            return style.standardIcon(icon_map[icon_name])
        
        return QIcon()
   
    def get_icon(self, icon_name: str, size: int = 24) -> QIcon:
        """Получить иконку по имени"""
        cache_key = f"{icon_name}_{size}"
        
        if cache_key in self.icons_cache:
            return self.icons_cache[cache_key]
       
        # Используем системную иконку
        icon = self._get_system_icon(icon_name)
        self.icons_cache[cache_key] = icon
        return icon
   
    # Предопределенные иконки
   
    def file_new(self, size: int = 24) -> QIcon:
        """Иконка 'Новый файл'"""
        return self.get_icon("file_new", size)
   
    def file_open(self, size: int = 24) -> QIcon:
        """Иконка 'Открыть файл'"""
        return self.get_icon("file_open", size)
   
    def file_save(self, size: int = 24) -> QIcon:
        """Иконка 'Сохранить'"""
        return self.get_icon("file_save", size)
   
    def file_print(self, size: int = 24) -> QIcon:
        """Иконка 'Печать'"""
        return self.get_icon("file_print", size)
   
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
        return self.get_icon("search_find", size)
   
    def search_replace(self, size: int = 24) -> QIcon:
        """Иконка 'Заменить'"""
        return self.get_icon("search_replace", size)
   
    def view_zoom_in(self, size: int = 24) -> QIcon:
        """Иконка 'Масштаб+'"""
        return self.get_icon("view_zoom_in", size)
   
    def view_zoom_out(self, size: int = 24) -> QIcon:
        """Иконка 'Масштаб-'"""
        return self.get_icon("view_zoom_out", size)
   
    def tool_settings(self, size: int = 24) -> QIcon:
        """Иконка 'Настройки'"""
        return self.get_icon("tool_settings", size)
   
    def tool_help(self, size: int = 24) -> QIcon:
        """Иконка 'Справка'"""
        return self.get_icon("tool_help", size)
   
    def app_icon(self, size: int = 256) -> QIcon:
        """Главная иконка приложения"""
        return self._get_system_icon("file_new")

# Глобальный экземпляр менеджера иконок
_icon_manager = None

def get_icon_manager() -> IconManager:
    """Получить глобальный менеджер иконок"""
    global _icon_manager
    if _icon_manager is None:
        _icon_manager = IconManager()
    return _icon_manager
