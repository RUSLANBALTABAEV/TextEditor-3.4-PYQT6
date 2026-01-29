"""
Менеджер панели инструментов
"""
from PyQt6.QtWidgets import QToolBar, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon


class ToolbarManager:
    """Управление панелью инструментов"""
    
    def __init__(self, editor):
        self.editor = editor
        self.toolbar = None
        
    def create_toolbar(self):
        """Создать панель инструментов"""
        self.toolbar = self.editor.addToolBar("Главная панель")
        self.toolbar.setMovable(False)
        
        # Файловые операции
        self.toolbar.addAction("Новый", self.editor.file_manager.new_file)
        self.toolbar.addAction("Открыть", self.editor.file_manager.open_file)
        self.toolbar.addAction("Сохранить", self.editor.file_manager.save_file)
        self.toolbar.addSeparator()
        
        # Вкладки
        self.toolbar.addAction("➕ Вкладка", self.editor.new_tab)
        self.toolbar.addAction("✕ Вкладка", self.editor.close_current_tab)
        self.toolbar.addSeparator()
        
        # Редактирование
        self.toolbar.addAction("Вырезать", self.editor.editor_commands.cut)
        self.toolbar.addAction("Копировать", self.editor.editor_commands.copy)
        self.toolbar.addAction("Вставить", self.editor.editor_commands.paste)
        self.toolbar.addSeparator()
        
        # Поиск
        self.toolbar.addAction("Найти", self.editor.show_search)
        self.toolbar.addAction("Заменить", self.editor.show_replace)
        self.toolbar.addSeparator()
        
        # Масштабирование
        self.toolbar.addAction("Увеличить", self.editor.editor_commands.zoom_in)
        self.toolbar.addAction("Уменьшить", self.editor.editor_commands.zoom_out)
        self.toolbar.addSeparator()
        
        # Печать
        self.toolbar.addAction("Печать", self.editor.file_manager.print_file)
