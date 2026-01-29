# main.py
"""
Текстовый редактор 3.4 - PyQt6 версия
Главная точка входа приложения
"""
import sys
from PyQt6.QtWidgets import QApplication
from app.texteditor import TextEditorApp
def main():
    app = QApplication(sys.argv)
    editor = TextEditorApp()
    editor.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
