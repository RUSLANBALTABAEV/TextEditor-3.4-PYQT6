"""
Менеджер меню приложения
"""
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtGui import QKeySequence


class MenuManager:
    """Управление меню"""
    
    def __init__(self, editor):
        self.editor = editor
        
    def create_menu(self):
        """Создать меню приложения"""
        menubar = self.editor.menuBar()
        
        # Меню Файл
        file_menu = menubar.addMenu("Файл")
        
        file_menu.addAction("Новый", self.editor.file_manager.new_file).setShortcut(QKeySequence.StandardKey.New)
        file_menu.addAction("Открыть", self.editor.file_manager.open_file).setShortcut(QKeySequence.StandardKey.Open)
        file_menu.addAction("Сохранить", self.editor.file_manager.save_file).setShortcut(QKeySequence.StandardKey.Save)
        file_menu.addAction("Сохранить как", self.editor.file_manager.save_as_file).setShortcut(QKeySequence.StandardKey.SaveAs)
        
        file_menu.addSeparator()
        file_menu.addAction("Новая вкладка", self.editor.new_tab).setShortcut("Ctrl+T")
        file_menu.addAction("Закрыть вкладку", self.editor.close_current_tab).setShortcut("Ctrl+W")
        
        file_menu.addSeparator()
        autosave_action = file_menu.addAction("Автосохранение")
        autosave_action.setCheckable(True)
        autosave_action.triggered.connect(self.editor.autosave_manager.toggle_autosave)
        
        file_menu.addSeparator()
        file_menu.addAction("Печать", self.editor.file_manager.print_file).setShortcut(QKeySequence.StandardKey.Print)
        file_menu.addSeparator()
        file_menu.addAction("Выход", self.editor.close).setShortcut(QKeySequence.StandardKey.Quit)
        
        # Меню Правка
        edit_menu = menubar.addMenu("Правка")
        
        edit_menu.addAction("Отменить", self.editor.editor_commands.undo).setShortcut(QKeySequence.StandardKey.Undo)
        edit_menu.addAction("Повторить", self.editor.editor_commands.redo).setShortcut(QKeySequence.StandardKey.Redo)
        edit_menu.addSeparator()
        edit_menu.addAction("Вырезать", self.editor.editor_commands.cut).setShortcut(QKeySequence.StandardKey.Cut)
        edit_menu.addAction("Копировать", self.editor.editor_commands.copy).setShortcut(QKeySequence.StandardKey.Copy)
        edit_menu.addAction("Вставить", self.editor.editor_commands.paste).setShortcut(QKeySequence.StandardKey.Paste)
        edit_menu.addSeparator()
        edit_menu.addAction("Найти", self.editor.show_search).setShortcut(QKeySequence.StandardKey.Find)
        edit_menu.addAction("Заменить", self.editor.show_replace).setShortcut(QKeySequence.StandardKey.Replace)
        edit_menu.addAction("Выделить все", self.editor.editor_commands.select_all).setShortcut(QKeySequence.StandardKey.SelectAll)
        
        # Меню Формат
        format_menu = menubar.addMenu("Формат")
        
        word_wrap_action = format_menu.addAction("Перенос слов")
        word_wrap_action.setCheckable(True)
        word_wrap_action.triggered.connect(self.editor.editor_commands.toggle_word_wrap)
        
        format_menu.addAction("Шрифт...", self.editor.editor_commands.change_font)
        format_menu.addSeparator()
        
        # Подменю Темы
        theme_menu = format_menu.addMenu("Тема")
        theme_menu.addAction("Светлая", lambda: self.editor.theme_manager.change_theme("light"))
        theme_menu.addAction("Темная", lambda: self.editor.theme_manager.change_theme("dark"))
        theme_menu.addAction("Синяя", lambda: self.editor.theme_manager.change_theme("blue"))
        theme_menu.addAction("Monokai", lambda: self.editor.theme_manager.change_theme("monokai"))
        
        # Меню Вид
        view_menu = menubar.addMenu("Вид")
        
        view_menu.addAction("Увеличить", self.editor.editor_commands.zoom_in).setShortcut("Ctrl++")
        view_menu.addAction("Уменьшить", self.editor.editor_commands.zoom_out).setShortcut("Ctrl+-")
        view_menu.addAction("Сбросить масштаб", self.editor.editor_commands.zoom_reset).setShortcut("Ctrl+0")
        
        # Меню Инструменты
        tools_menu = menubar.addMenu("Инструменты")
        
        tools_menu.addAction("Статистика", self.editor.editor_commands.show_statistics)
        tools_menu.addAction("Вставить дату/время", self.editor.editor_commands.insert_datetime).setShortcut("F5")
        
        # Меню Справка
        help_menu = menubar.addMenu("Справка")
        
        help_menu.addAction("Справка", self.show_help).setShortcut("F1")
        help_menu.addAction("О программе", self.show_about)
        help_menu.addAction("Лицензия", self.show_license)
        
    def show_help(self):
        """Показать справку"""
        help_text = """
<h2>Текстовый редактор 3.4 - PyQt6</h2>

<h3>Основные возможности:</h3>
<ul>
<li>Работа с несколькими вкладками (Ctrl+T для новой вкладки)</li>
<li>Автосохранение и восстановление сессий</li>
<li>Поиск и замена текста (Ctrl+F / Ctrl+H)</li>
<li>Несколько цветовых тем</li>
<li>Изменение размера шрифта (Ctrl+/ / Ctrl+-)</li>
<li>Статистика документа</li>
<li>Печать документов</li>
<li>Поддержка различных кодировок</li>
</ul>

<h3>Горячие клавиши:</h3>
<table>
<tr><td>Ctrl+N</td><td>Новый файл</td></tr>
<tr><td>Ctrl+O</td><td>Открыть файл</td></tr>
<tr><td>Ctrl+S</td><td>Сохранить</td></tr>
<tr><td>Ctrl+T</td><td>Новая вкладка</td></tr>
<tr><td>Ctrl+W</td><td>Закрыть вкладку</td></tr>
<tr><td>Ctrl+F</td><td>Поиск</td></tr>
<tr><td>Ctrl+H</td><td>Замена</td></tr>
<tr><td>F5</td><td>Вставить дату/время</td></tr>
</table>
        """
        
        QMessageBox.information(self.editor, "Справка", help_text)
        
    def show_about(self):
        """Показать информацию о программе"""
        about_text = """
<h2>Текстовый редактор 3.4</h2>

<p><b>Версия:</b> 3.4 (PyQt6)</p>
<p><b>Лицензия:</b> MIT</p>

<p>Современный текстовый редактор с поддержкой множества функций 
для комфортной работы с текстом и кодом.</p>

<h3>Основные функции:</h3>
<ul>
<li>Многодокументный интерфейс с вкладками</li>
<li>Автосохранение документов</li>
<li>Несколько тем оформления</li>
<li>Функции поиска и замены</li>
<li>Статистика документов</li>
<li>Поддержка различных форматов</li>
</ul>

<p><b>Разработчик:</b> Text Editor Team</p>
        """
        
        QMessageBox.information(self.editor, "О программе", about_text)
        
    def show_license(self):
        """Показать лицензию"""
        license_text = """
MIT License

Copyright (c) 2024 Text Editor 3.4

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
        """
        
        QMessageBox.information(self.editor, "Лицензия MIT", license_text)
