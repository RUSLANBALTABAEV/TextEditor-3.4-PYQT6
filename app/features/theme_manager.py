"""
Менеджер тем оформления
"""
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget
from app.utils.constants import THEMES


class ThemeManager:
    """Управление темами приложения"""
    
    def __init__(self, editor):
        self.editor = editor
        
    def change_theme(self, theme_name):
        """Изменить тему"""
        if theme_name in THEMES:
            self.editor.theme = theme_name
            self.apply_theme()
            
    def apply_theme(self):
        """Применить текущую тему"""
        theme = THEMES.get(self.editor.theme, THEMES['light'])
        
        # Применяем цвета к редактору
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data:
                text_edit = tab_data['text_edit']
                
                # Установка цветов
                text_edit.setStyleSheet(f"""
                    QTextEdit {{
                        background-color: {theme['bg']};
                        color: {theme['fg']};
                        selection-background-color: {theme.get('selection', '#add6ff')};
                    }}
                """)
        
        # Применяем тему к главному окну
        self.editor.setStyleSheet(f"""
            QMainWindow {{
                background-color: {theme['bg']};
            }}
            QMenuBar {{
                background-color: {theme['bg']};
                color: {theme['fg']};
            }}
            QMenu {{
                background-color: {theme['bg']};
                color: {theme['fg']};
            }}
            QToolBar {{
                background-color: {theme['bg']};
                border: none;
            }}
            QPushButton {{
                background-color: {theme.get('button_bg', theme['bg'])};
                color: {theme['fg']};
                border: 1px solid #cccccc;
                padding: 2px;
                border-radius: 2px;
            }}
            QPushButton:hover {{
                background-color: {theme.get('button_hover', '#e0e0e0')};
            }}
            QLineEdit {{
                background-color: {theme['bg']};
                color: {theme['fg']};
                border: 1px solid #cccccc;
                padding: 2px;
            }}
            QLabel {{
                color: {theme['fg']};
            }}
        """)
        
    def get_theme_colors(self):
        """Получить цвета текущей темы"""
        return THEMES.get(self.editor.theme, THEMES['light'])
