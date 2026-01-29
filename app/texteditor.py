# app/texteditor.py
"""
Основной класс текстового редактора PyQt6
"""
import os
import json
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QTextEdit, QLabel, QSplitter,
                             QMessageBox, QFileDialog, QInputDialog)
from PyQt6.QtCore import Qt, QTimer, QSettings, QSize, QEvent
from PyQt6.QtGui import QFont, QIcon, QAction, QKeySequence, QShortcut
from app.core.file_manager import FileManager
from app.core.editor_commands import EditorCommands
from app.core.session_manager import SessionManager
from app.features.search_replace import SearchReplaceWidget
from app.features.autosave import AutoSaveManager
from app.features.theme_manager import ThemeManager
from app.ui.menu import MenuManager
from app.ui.toolbar import ToolbarManager
from app.ui.statusbar import StatusBarManager
from app.utils.constants import *

class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
       
        # Инициализация настроек
        self.settings = QSettings("TextEditor", "TextEditor3.4")
        self.current_file = None
        self.auto_save_enabled = False
        self.auto_save_interval = AUTOSAVE_INTERVAL
        self.theme = DEFAULT_THEME
        self.tab_data = {}
        self.current_tab_index = 0
       
        # Создание директорий
        self.setup_directories()
       
        # Инициализация компонентов
        self.file_manager = FileManager(self)
        self.editor_commands = EditorCommands(self)
        self.session_manager = SessionManager(self)
        self.autosave_manager = AutoSaveManager(self)
        self.theme_manager = ThemeManager(self)
        self.menu_manager = MenuManager(self)
        self.toolbar_manager = ToolbarManager(self)
        self.statusbar_manager = StatusBarManager(self)
       
        # Настройка UI
        self.setup_ui()
        self.setup_autosave_timer()
        self.setup_bindings()
       
        # Загрузка сессии
        self.session_manager.load_session()
       
        # Восстановление размеров окна
        self.restore_window_geometry()
       
    def setup_directories(self):
        """Создает необходимые директории"""
        self.backup_dir = Path.home() / ".texteditor" / "backups"
        self.plugins_dir = Path.home() / ".texteditor" / "plugins"
        self.config_dir = Path.home() / ".texteditor"
       
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
       
        self.session_file = self.config_dir / "session.json"
        self.theme_file = self.config_dir / "theme.json"
       
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Текстовый Редактор 3.4")
        self.setObjectName("TextEditorApp")  # ✅ ИСПРАВЛЕНО: Установляем objectName для окна
        self.setGeometry(100, 100, 1200, 700)
       
        # Загрузка иконки
        self.setup_icon()
       
        # Создание центрального виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
       
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
       
        # Создание вкладок
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
       
        # Добавляем первую пустую вкладку
        self.new_tab()
       
        main_layout.addWidget(self.tab_widget)
       
        # Панель поиска и замены
        self.search_replace_widget = SearchReplaceWidget(self)
        main_layout.addWidget(self.search_replace_widget)
        self.search_replace_widget.hide()
       
        # Создание меню, панели инструментов и статусбара
        self.menu_manager.create_menu()
        self.toolbar_manager.create_toolbar()
        self.statusbar_manager.create_statusbar()
       
        # Применение темы
        self.theme_manager.apply_theme()
       
    def setup_icon(self):
        """Загрузка иконки приложения"""
        icon_path = Path(__file__).parent.parent / "TextEditor.ico"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
           
    def new_tab(self, file_path=None, content=None):
        """Создание новой вкладки"""
        text_edit = QTextEdit()
        text_edit.setFont(QFont(DEFAULT_FONT[0], DEFAULT_FONT[1]))
        text_edit.textChanged.connect(self.on_text_changed)
        text_edit.cursorPositionChanged.connect(self.update_status)
        
        # Разрешаем горячие клавиши в текстовом поле
        text_edit.installEventFilter(self)
       
        if content:
            text_edit.setPlainText(content)
       
        # Определяем имя вкладки
        if file_path:
            tab_name = Path(file_path).name
        else:
            tab_name = f"Новый {self.tab_widget.count() + 1}"
       
        # Храним метаданные в словаре
        tab_index = self.tab_widget.addTab(text_edit, tab_name)
       
        self.tab_data[tab_index] = {
            'file_path': file_path,
            'modified': False,
            'name': tab_name,
            'text_edit': text_edit
        }
       
        self.tab_widget.setCurrentIndex(tab_index)
        return tab_index
       
    def close_tab(self, index):
        """Закрытие вкладки"""
        if self.tab_widget.count() <= 1:
            return
       
        # Проверяем сохранение
        tab_data = self.get_tab_data(index)
        if tab_data and tab_data.get('modified'):
            text_edit = tab_data['text_edit']
            if text_edit.toPlainText().strip():
                reply = QMessageBox.question(
                    self,
                    "Сохранение",
                    f"Сохранить изменения в {tab_data['name']}?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
                )
               
                if reply == QMessageBox.StandardButton.Cancel:
                    return
                elif reply == QMessageBox.StandardButton.Yes:
                    self.current_tab_index = index
                    self.file_manager.save_file()
       
        self.tab_widget.removeTab(index)
        if index in self.tab_data:
            del self.tab_data[index]
           
    def on_tab_changed(self, index):
        """Обработчик смены вкладки"""
        self.current_tab_index = index
        self.update_status()
        self.update_window_title()
       
    def on_text_changed(self):
        """Обработчик изменения текста"""
        index = self.tab_widget.currentIndex()
        tab_data = self.get_tab_data(index)
        if tab_data:
            tab_data['modified'] = True
            self.update_window_title()
           
    def get_current_text_edit(self):
        """Возвращает текущий QTextEdit"""
        return self.tab_widget.currentWidget()
       
    def get_tab_data(self, index):
        """Возвращает данные вкладки"""
        return self.tab_data.get(index)
       
    def get_current_tab_data(self):
        """Возвращает данные текущей вкладки"""
        return self.get_tab_data(self.tab_widget.currentIndex())
       
    def update_status(self):
        """Обновление статусбара"""
        text_edit = self.get_current_text_edit()
        if text_edit:
            cursor = text_edit.textCursor()
            line = cursor.blockNumber() + 1
            column = cursor.positionInBlock() + 1
           
            text = text_edit.toPlainText()
            total_lines = len(text.split('\n'))
            words = len(text.split())
            chars = len(text)
           
            tab_data = self.get_current_tab_data()
            modified = " [Изменен]" if tab_data and tab_data.get('modified') else ""
            file_path = tab_data.get('file_path', '') if tab_data else ''
           
            status_text = (
                f"Строка: {line}, Колонка: {column} | "
                f"Строк: {total_lines} | Слов: {words} | Символов: {chars}"
                f"{modified}"
            )
           
            self.statusbar_manager.set_text(status_text)
           
    def update_window_title(self):
        """Обновление заголовка окна"""
        tab_data = self.get_current_tab_data()
        if tab_data:
            name = tab_data['name']
            modified = "*" if tab_data['modified'] else ""
            self.setWindowTitle(f"Текстовый Редактор 3.4 - {name}{modified}")
        else:
            self.setWindowTitle("Текстовый Редактор 3.4")
       
    def setup_bindings(self):
        """Привязка горячих клавиш - ИСПРАВЛЕНО"""
        # Файловые операции
        self.shortcut_new = QShortcut(QKeySequence.StandardKey.New, self)
        self.shortcut_new.activated.connect(self.file_manager.new_file)
        
        self.shortcut_open = QShortcut(QKeySequence.StandardKey.Open, self)
        self.shortcut_open.activated.connect(self.file_manager.open_file)
        
        self.shortcut_save = QShortcut(QKeySequence.StandardKey.Save, self)
        self.shortcut_save.activated.connect(self.file_manager.save_file)
        
        self.shortcut_save_as = QShortcut(QKeySequence.StandardKey.SaveAs, self)
        self.shortcut_save_as.activated.connect(self.file_manager.save_as_file)
        
        self.shortcut_print = QShortcut(QKeySequence.StandardKey.Print, self)
        self.shortcut_print.activated.connect(self.file_manager.print_file)
        
        self.shortcut_quit = QShortcut(QKeySequence.StandardKey.Quit, self)
        self.shortcut_quit.activated.connect(self.close)
       
        # Редактирование
        self.shortcut_undo = QShortcut(QKeySequence.StandardKey.Undo, self)
        self.shortcut_undo.activated.connect(self.editor_commands.undo)
        
        self.shortcut_redo = QShortcut(QKeySequence.StandardKey.Redo, self)
        self.shortcut_redo.activated.connect(self.editor_commands.redo)
        
        self.shortcut_cut = QShortcut(QKeySequence.StandardKey.Cut, self)
        self.shortcut_cut.activated.connect(self.editor_commands.cut)
        
        self.shortcut_copy = QShortcut(QKeySequence.StandardKey.Copy, self)
        self.shortcut_copy.activated.connect(self.editor_commands.copy)
        
        self.shortcut_paste = QShortcut(QKeySequence.StandardKey.Paste, self)
        self.shortcut_paste.activated.connect(self.editor_commands.paste)
        
        self.shortcut_select_all = QShortcut(QKeySequence.StandardKey.SelectAll, self)
        self.shortcut_select_all.activated.connect(self.editor_commands.select_all)
        
        self.shortcut_find = QShortcut(QKeySequence.StandardKey.Find, self)
        self.shortcut_find.activated.connect(self.show_search)
        
        self.shortcut_replace = QShortcut(QKeySequence.StandardKey.Replace, self)
        self.shortcut_replace.activated.connect(self.show_replace)
       
        # Вкладки
        self.shortcut_new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcut_new_tab.activated.connect(self.new_tab)
        
        self.shortcut_close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        self.shortcut_close_tab.activated.connect(self.close_current_tab)
       
        # Масштабирование
        self.shortcut_zoom_in = QShortcut(QKeySequence.StandardKey.ZoomIn, self)
        self.shortcut_zoom_in.activated.connect(self.editor_commands.zoom_in)
        
        self.shortcut_zoom_out = QShortcut(QKeySequence.StandardKey.ZoomOut, self)
        self.shortcut_zoom_out.activated.connect(self.editor_commands.zoom_out)
        
        self.shortcut_zoom_reset = QShortcut(QKeySequence("Ctrl+0"), self)
        self.shortcut_zoom_reset.activated.connect(self.editor_commands.zoom_reset)
       
        # Другое
        self.shortcut_datetime = QShortcut(QKeySequence("F5"), self)
        self.shortcut_datetime.activated.connect(self.editor_commands.insert_datetime)
        
        self.shortcut_help = QShortcut(QKeySequence("F1"), self)
        self.shortcut_help.activated.connect(self.menu_manager.show_help)
    
    def eventFilter(self, obj, event):
        """Перехват событий для горячих клавиш в текстовом поле"""
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            modifiers = event.modifiers()
            
            # Проверяем если это текстовый редактор
            if isinstance(obj, QTextEdit):
                # Ctrl+Z - отмена (стандартная)
                if key == Qt.Key.Key_Z and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.editor_commands.undo()
                    return True
                # Ctrl+Y - повтор (стандартная)
                elif key == Qt.Key.Key_Y and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.editor_commands.redo()
                    return True
                # Ctrl+F - поиск
                elif key == Qt.Key.Key_F and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.show_search()
                    return True
                # Ctrl+H - замена
                elif key == Qt.Key.Key_H and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.show_replace()
                    return True
                # Ctrl++ - увеличить
                elif key == Qt.Key.Key_Plus and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.editor_commands.zoom_in()
                    return True
                # Ctrl+- - уменьшить
                elif key == Qt.Key.Key_Minus and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.editor_commands.zoom_out()
                    return True
                # Ctrl+0 - сброс масштаба
                elif key == Qt.Key.Key_0 and modifiers == Qt.KeyboardModifier.ControlModifier:
                    self.editor_commands.zoom_reset()
                    return True
                # F5 - дата/время
                elif key == Qt.Key.Key_F5:
                    self.editor_commands.insert_datetime()
                    return True
        
        return super().eventFilter(obj, event)
       
    def show_search(self):
        """Показать панель поиска"""
        self.search_replace_widget.show_search()
       
    def show_replace(self):
        """Показать панель замены"""
        self.search_replace_widget.show_replace()
       
    def close_current_tab(self):
        """Закрыть текущую вкладку"""
        self.close_tab(self.tab_widget.currentIndex())
       
    def setup_autosave_timer(self):
        """Настройка таймера для автосохранения"""
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave_manager.autosave)
       
    def closeEvent(self, event):
        """Обработчик закрытия приложения"""
        if self.check_save_all():
            self.session_manager.save_session()
            self.save_window_geometry()
            event.accept()
        else:
            event.ignore()
           
    def check_save_all(self):
        """Проверка сохранения всех вкладок"""
        for i in range(self.tab_widget.count()):
            tab_data = self.get_tab_data(i)
            if tab_data and tab_data.get('modified'):
                text_edit = tab_data['text_edit']
                if text_edit.toPlainText().strip():
                    self.tab_widget.setCurrentIndex(i)
                    reply = QMessageBox.question(
                        self,
                        "Сохранение",
                        f"Сохранить изменения в {tab_data['name']}?",
                        QMessageBox.StandardButton.Yes |
                        QMessageBox.StandardButton.No |
                        QMessageBox.StandardButton.Cancel
                    )
                   
                    if reply == QMessageBox.StandardButton.Cancel:
                        return False
                    elif reply == QMessageBox.StandardButton.Yes:
                        self.file_manager.save_file()
        return True
       
    def save_window_geometry(self):
        """Сохранение размеров окна"""
        self.settings.setValue("geometry", self.saveGeometry())
        self.settings.setValue("windowState", self.saveState())
       
    def restore_window_geometry(self):
        """Восстановление размеров окна"""
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)
        windowState = self.settings.value("windowState")
        if windowState:
            self.restoreState(windowState)
