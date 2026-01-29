"""
Команды редактирования текста
"""
from datetime import datetime
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSpinBox, QListWidget, QListWidgetItem, QPushButton, QMessageBox, QFontDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class EditorCommands:
    """Команды редактирования"""
    
    def __init__(self, editor):
        self.editor = editor
        
    def undo(self):
        """Отмена"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.undo()
            
    def redo(self):
        """Повтор"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.redo()
            
    def cut(self):
        """Вырезать"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.cut()
            
    def copy(self):
        """Копировать"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.copy()
            
    def paste(self):
        """Вставить"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.paste()
            
    def delete(self):
        """Удалить выделенный текст"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.textCursor().removeSelectedText()
            
    def select_all(self):
        """Выделить весь текст"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.selectAll()
            
    def insert_datetime(self):
        """Вставить дату и время"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            text_edit.insertPlainText(dt_string)
            
    def toggle_word_wrap(self):
        """Переключить перенос слов"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            text_edit.setWordWrapMode(
                not text_edit.wordWrapMode()
            )
            
    def change_font(self):
        """Изменить шрифт"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
        
        current_font = text_edit.font()
        font, ok = QFontDialog.getFont(current_font, self.editor)
        
        if ok:
            # Применяем шрифт ко всем вкладкам
            for i in range(self.editor.tab_widget.count()):
                tab_data = self.editor.get_tab_data(i)
                if tab_data:
                    tab_data['text_edit'].setFont(font)
                    
    def zoom_in(self):
        """Увеличить размер шрифта"""
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data:
                font = tab_data['text_edit'].font()
                font.setPointSize(font.pointSize() + 1)
                tab_data['text_edit'].setFont(font)
                
    def zoom_out(self):
        """Уменьшить размер шрифта"""
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data:
                font = tab_data['text_edit'].font()
                new_size = max(8, font.pointSize() - 1)
                font.setPointSize(new_size)
                tab_data['text_edit'].setFont(font)
                
    def zoom_reset(self):
        """Сбросить масштаб"""
        from app.utils.constants import DEFAULT_FONT
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data:
                font = QFont(DEFAULT_FONT[0], DEFAULT_FONT[1])
                tab_data['text_edit'].setFont(font)
                
    def show_statistics(self):
        """Показать статистику документа"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
        
        text = text_edit.toPlainText()
        lines = len(text.split('\n'))
        words = len(text.split())
        chars = len(text)
        chars_no_spaces = len(text.replace(' ', '').replace('\n', ''))
        
        QMessageBox.information(
            self.editor,
            "Статистика документа",
            f"Строк: {lines}\n"
            f"Слов: {words}\n"
            f"Символов: {chars}\n"
            f"Символов (без пробелов): {chars_no_spaces}"
        )
