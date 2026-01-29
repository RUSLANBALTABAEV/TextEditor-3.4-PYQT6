# app/ui/toolbar.py
"""
Менеджер панели инструментов
"""
from PyQt6.QtWidgets import QToolBar, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from app.utils.icon_manager import get_icon_manager
class ToolbarManager:
    """Управление панелью инструментов"""
   
    def __init__(self, editor):
        self.editor = editor
        self.toolbar = None
        self.icons = get_icon_manager()
       
    def create_toolbar(self):
        """Создать панель инструментов"""
        self.toolbar = self.editor.addToolBar("Главная панель")
        self.toolbar.setMovable(False)
        self.toolbar.setIconSize(self.toolbar.iconSize())
       
        # Файловые операции
        action = self.toolbar.addAction(self.icons.file_new(), "Новый")
        action.triggered.connect(self.editor.file_manager.new_file)
       
        action = self.toolbar.addAction(self.icons.file_open(), "Открыть")
        action.triggered.connect(self.editor.file_manager.open_file)
       
        action = self.toolbar.addAction(self.icons.file_save(), "Сохранить")
        action.triggered.connect(self.editor.file_manager.save_file)
       
        self.toolbar.addSeparator()
       
        # Вкладки
        action = self.toolbar.addAction(self.icons.get_icon("tab_new"), "Новая вкладка")
        action.triggered.connect(self.editor.new_tab)
       
        action = self.toolbar.addAction(self.icons.get_icon("tab_close"), "Закрыть")
        action.triggered.connect(self.editor.close_current_tab)
       
        self.toolbar.addSeparator()
       
        # Редактирование
        action = self.toolbar.addAction(self.icons.edit_cut(), "Вырезать")
        action.triggered.connect(self.editor.editor_commands.cut)
       
        action = self.toolbar.addAction(self.icons.edit_copy(), "Копировать")
        action.triggered.connect(self.editor.editor_commands.copy)
       
        action = self.toolbar.addAction(self.icons.edit_paste(), "Вставить")
        action.triggered.connect(self.editor.editor_commands.paste)
       
        self.toolbar.addSeparator()
       
        # Поиск
        action = self.toolbar.addAction(self.icons.search_find(), "Найти")
        action.triggered.connect(self.editor.show_search)
       
        action = self.toolbar.addAction(self.icons.search_replace(), "Заменить")
        action.triggered.connect(self.editor.show_replace)
       
        self.toolbar.addSeparator()
       
        # Масштабирование
        action = self.toolbar.addAction(self.icons.view_zoom_in(), "Увеличить")
        action.triggered.connect(self.editor.editor_commands.zoom_in)
       
        action = self.toolbar.addAction(self.icons.view_zoom_out(), "Уменьшить")
        action.triggered.connect(self.editor.editor_commands.zoom_out)
       
        self.toolbar.addSeparator()
       
        # Печать
        action = self.toolbar.addAction(self.icons.file_print(), "Печать")
        action.triggered.connect(self.editor.file_manager.print_file)
