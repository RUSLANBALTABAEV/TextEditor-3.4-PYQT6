# app/utils/constants.py
# Константы приложения PyQt6
# Настройки по умолчанию
DEFAULT_FONT = ('Consolas', 11)
DEFAULT_THEME = 'light'
AUTOSAVE_INTERVAL = 300000 # 5 минут в миллисекундах
# Поддерживаемые типы файлов
SUPPORTED_FILES = [
    ("Текстовые файлы", "*.txt"),
    ("Документы Python", "*.py"),
    ("HTML файлы", "*.html *.htm"),
    ("CSS файлы", "*.css"),
    ("JavaScript файлы", "*.js"),
    ("JSON файлы", "*.json"),
    ("Markdown файлы", "*.md"),
    ("Все файлы", "*.*")
]
# Темы
THEMES = {
    'light': {
        'bg': '#ffffff',
        'fg': '#000000',
        'line_numbers_bg': '#f0f0f0',
        'line_numbers_fg': '#666666',
        'selection': '#add6ff'
    },
    'dark': {
        'bg': '#1e1e1e',
        'fg': '#e0e0e0',
        'line_numbers_bg': '#252526',
        'line_numbers_fg': '#858585',
        'selection': '#264f78'
    },
    'blue': {
        'bg': '#e6f3ff',
        'fg': '#1a1a1a',
        'line_numbers_bg': '#d4e7f5',
        'line_numbers_fg': '#3a5f80',
        'selection': '#b3d9ff'
    },
    'monokai': {
        'bg': '#272822',
        'fg': '#f8f8f2',
        'line_numbers_bg': '#3e3d32',
        'line_numbers_fg': '#90908a',
        'selection': '#49483e'
    }
}
# Размеры интерфейса
DEFAULT_WINDOW_WIDTH = 1200
DEFAULT_WINDOW_HEIGHT = 700
TOOLBAR_ICON_SIZE = 16
