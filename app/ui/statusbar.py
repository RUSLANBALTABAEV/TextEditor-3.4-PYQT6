"""
Менеджер строки состояния
"""
from PyQt6.QtWidgets import QStatusBar, QLabel


class StatusBarManager:
    """Управление строкой состояния"""
    
    def __init__(self, editor):
        self.editor = editor
        self.status_label = None
        
    def create_statusbar(self):
        """Создать строку состояния"""
        self.status_label = QLabel("Готово | Строк: 1 | Слов: 0 | Символов: 0")
        self.editor.statusBar().addWidget(self.status_label)
        
    def set_text(self, text):
        """Установить текст в статусбаре"""
        if self.status_label:
            self.status_label.setText(text)
            
    def update_status(self):
        """Обновить статусбар"""
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            cursor = text_edit.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.positionInBlock() + 1
            
            text = text_edit.toPlainText()
            total_lines = len(text.split('\n'))
            words = len(text.split())
            chars = len(text)
            
            status_text = (
                f"Строка: {line}, Колонка: {column} | "
                f"Строк: {total_lines} | Слов: {words} | Символов: {chars}"
            )
            
            self.set_text(status_text)
