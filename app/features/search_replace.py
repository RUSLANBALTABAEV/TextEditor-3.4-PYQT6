# app/features/search_replace.py
"""
Виджет поиска и замены
"""
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLineEdit, QPushButton,
                             QLabel, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QTextCursor, QColor
class SearchReplaceWidget(QWidget):
    """Виджет для поиска и замены текста"""
   
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.current_match = None
        self.search_visible = False
        self.replace_visible = False
       
        self.setup_ui()
       
    def setup_ui(self):
        """Настройка UI"""
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
       
        # Поле поиска
        main_layout.addWidget(QLabel("Найти:"))
        self.find_input = QLineEdit()
        self.find_input.returnPressed.connect(self.find_next)
        main_layout.addWidget(self.find_input)
       
        # Кнопки поиска
        find_btn = QPushButton("Найти")
        find_btn.clicked.connect(self.find_next)
        main_layout.addWidget(find_btn)
       
        find_prev_btn = QPushButton("Найти предыдущее")
        find_prev_btn.clicked.connect(self.find_previous)
        main_layout.addWidget(find_prev_btn)
       
        # Поле замены (скрыто по умолчанию)
        main_layout.addWidget(QLabel("Заменить на:"))
        self.replace_input = QLineEdit()
        self.replace_input.returnPressed.connect(self.replace_next)
        self.replace_input.hide()
        main_layout.addWidget(self.replace_input)
        self.replace_label = main_layout.itemAt(main_layout.count() - 2).widget()
        self.replace_label.hide()
       
        # Кнопки замены
        self.replace_btn = QPushButton("Заменить")
        self.replace_btn.clicked.connect(self.replace_next)
        self.replace_btn.hide()
        main_layout.addWidget(self.replace_btn)
       
        self.replace_all_btn = QPushButton("Заменить все")
        self.replace_all_btn.clicked.connect(self.replace_all)
        self.replace_all_btn.hide()
        main_layout.addWidget(self.replace_all_btn)
       
        # Опции
        self.case_sensitive = QCheckBox("Учитывать регистр")
        self.case_sensitive.hide()
        main_layout.addWidget(self.case_sensitive)
       
        self.whole_words = QCheckBox("Целые слова")
        self.whole_words.hide()
        main_layout.addWidget(self.whole_words)
       
        # Кнопка закрытия
        close_btn = QPushButton("✕")
        close_btn.setMaximumWidth(30)
        close_btn.clicked.connect(self.hide)
        main_layout.addWidget(close_btn)
       
        main_layout.addStretch()
       
    def show_search(self):
        """Показать панель поиска"""
        self.show()
        self.search_visible = True
        self.replace_input.hide()
        self.replace_label.hide()
        self.replace_btn.hide()
        self.replace_all_btn.hide()
        self.case_sensitive.show()
        self.whole_words.show()
        self.find_input.setFocus()
        self.find_input.selectAll()
       
    def show_replace(self):
        """Показать панель замены"""
        self.show()
        self.search_visible = True
        self.replace_visible = True
        self.replace_input.show()
        self.replace_label.show()
        self.replace_btn.show()
        self.replace_all_btn.show()
        self.case_sensitive.show()
        self.whole_words.show()
        self.replace_input.setFocus()
       
    def find_next(self):
        """Найти следующее совпадение"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
       
        search_text = self.find_input.text()
        if not search_text:
            return
       
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.EndOfSelection)
       
        # Параметры поиска
        flags = 0
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
       
        # Ищем текст
        from PyQt6.QtGui import QTextDocument
        document = text_edit.document()
        cursor = document.find(search_text, cursor, QTextDocument.FindFlag(flags))
       
        if not cursor.isNull():
            text_edit.setTextCursor(cursor)
            text_edit.setFocus()
        else:
            # Ищем с начала
            cursor = QTextCursor(document)
            cursor = document.find(search_text, cursor, QTextDocument.FindFlag(flags))
           
            if not cursor.isNull():
                text_edit.setTextCursor(cursor)
            else:
                QMessageBox.information(self.editor, "Поиск", "Текст не найден")
               
    def find_previous(self):
        """Найти предыдущее совпадение"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
       
        search_text = self.find_input.text()
        if not search_text:
            return
       
        cursor = text_edit.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.StartOfSelection)
       
        # Параметры поиска
        flags = QTextDocument.FindFlag.FindBackward
        if self.case_sensitive.isChecked():
            flags |= QTextDocument.FindFlag.FindCaseSensitively
        if self.whole_words.isChecked():
            flags |= QTextDocument.FindFlag.FindWholeWords
       
        from PyQt6.QtGui import QTextDocument
        document = text_edit.document()
        cursor = document.find(search_text, cursor, flags)
       
        if not cursor.isNull():
            text_edit.setTextCursor(cursor)
        else:
            QMessageBox.information(self.editor, "Поиск", "Текст не найден")
           
    def replace_next(self):
        """Заменить текущее совпадение"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
       
        cursor = text_edit.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
       
        self.find_next()
       
    def replace_all(self):
        """Заменить все совпадения"""
        text_edit = self.editor.get_current_text_edit()
        if not text_edit:
            return
       
        search_text = self.find_input.text()
        replace_text = self.replace_input.text()
       
        if not search_text:
            return
       
        content = text_edit.toPlainText()
        count = content.count(search_text)
       
        if count == 0:
            QMessageBox.information(self.editor, "Замена", "Текст не найден")
            return
       
        new_content = content.replace(search_text, replace_text)
        text_edit.setPlainText(new_content)
       
        QMessageBox.information(
            self.editor,
            "Замена",
            f"Заменено {count} совпадений"
        )
       
    def hideEvent(self, event):
        """При скрытии очищаем выделение"""
        super().hideEvent(event)
        text_edit = self.editor.get_current_text_edit()
        if text_edit:
            cursor = text_edit.textCursor()
            cursor.clearSelection()
            text_edit.setTextCursor(cursor)
