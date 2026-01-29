# app/core/file_manager.py
"""
Менеджер файлов для работы с документами
"""
import os
from pathlib import Path
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog
from PyQt6.QtGui import QTextDocument
class FileManager:
    """Управление файлами (открытие, сохранение, печать)"""
   
    def __init__(self, editor):
        self.editor = editor
       
    def new_file(self):
        """Создание нового файла"""
        current_index = self.editor.tab_widget.currentIndex()
        current_data = self.editor.get_current_tab_data()
       
        # Если текущая вкладка пуста, используем её
        if current_data and not current_data['modified'] and not current_data['file_path']:
            return
       
        self.editor.new_tab()
       
    def open_file(self, file_path=None):
        """Открытие файла"""
        if not file_path:
            file_path, _ = QFileDialog.getOpenFileName(
                self.editor,
                "Открыть файл",
                "",
                ";;".join([f"{name} ({ext})" for name, ext in __import__('app.utils.constants', fromlist=['SUPPORTED_FILES']).SUPPORTED_FILES])
            )
       
        if file_path:
            try:
                # Пробуем разные кодировки
                encodings = ['utf-8', 'cp1251', 'iso-8859-1', 'windows-1252']
                content = None
               
                for encoding in encodings:
                    try:
                        with open(file_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        break
                    except UnicodeDecodeError:
                        continue
               
                if content is None:
                    with open(file_path, 'rb') as f:
                        content = f.read().decode('latin-1')
               
                # Создаем новую вкладку
                self.editor.new_tab(file_path, content)
               
            except Exception as e:
                QMessageBox.critical(
                    self.editor,
                    "Ошибка",
                    f"Не удалось открыть файл:\n{str(e)}"
                )
               
    def save_file(self):
        """Сохранение текущего файла"""
        current_data = self.editor.get_current_tab_data()
        if not current_data:
            return
       
        file_path = current_data['file_path']
       
        if file_path:
            try:
                text_edit = current_data['text_edit']
                content = text_edit.toPlainText()
               
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
               
                current_data['modified'] = False
                self.editor.update_window_title()
                self.editor.statusbar_manager.set_text("Файл сохранен")
               
            except Exception as e:
                QMessageBox.critical(
                    self.editor,
                    "Ошибка сохранения",
                    f"Не удалось сохранить файл:\n{str(e)}"
                )
        else:
            self.save_as_file()
           
    def save_as_file(self):
        """Сохранение файла с новым именем"""
        file_path, _ = QFileDialog.getSaveFileName(
            self.editor,
            "Сохранить файл как",
            "",
            ";;".join([f"{name} ({ext})" for name, ext in __import__('app.utils.constants', fromlist=['SUPPORTED_FILES']).SUPPORTED_FILES])
        )
       
        if file_path:
            try:
                text_edit = self.editor.get_current_text_edit()
                content = text_edit.toPlainText()
               
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
               
                current_data = self.editor.get_current_tab_data()
                if current_data:
                    current_data['file_path'] = file_path
                    current_data['modified'] = False
                    current_data['name'] = Path(file_path).name
                   
                    # Обновляем вкладку
                    current_index = self.editor.tab_widget.currentIndex()
                    self.editor.tab_widget.setTabText(current_index, current_data['name'])
                   
                self.editor.update_window_title()
                self.editor.statusbar_manager.set_text("Файл сохранен")
               
            except Exception as e:
                QMessageBox.critical(
                    self.editor,
                    "Ошибка сохранения",
                    f"Не удалось сохранить файл:\n{str(e)}"
                )
               
    def print_file(self):
        """Печать документа"""
        try:
            text_edit = self.editor.get_current_text_edit()
            if not text_edit:
                return
           
            printer = QPrinter()
            dialog = QPrintDialog(printer, self.editor)
           
            if dialog.exec() == QFileDialog.DialogCode.Accepted:
                document = QTextDocument()
                document.setPlainText(text_edit.toPlainText())
                document.print(printer)
                QMessageBox.information(self.editor, "Печать", "Документ отправлен на печать")
               
        except Exception as e:
            QMessageBox.critical(
                self.editor,
                "Ошибка печати",
                f"Не удалось напечатать документ:\n{str(e)}"
            )
