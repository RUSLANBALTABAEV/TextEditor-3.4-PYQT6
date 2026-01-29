# Миграция с Tkinter на PyQt6 - Документация

## 📊 Сравнение Tkinter vs PyQt6

### Преимущества PyQt6
1. **Нативный внешний вид** - использует компоненты операционной системы
2. **Большой набор виджетов** - значительно более богатая библиотека UI компонентов
3. **Лучшая производительность** - быстрее работает с большими объемами данных
4. **Профессиональный внешний вид** - поддержка стилей CSS
5. **Кроссплатформенность** - одинаковый вид на Windows, macOS, Linux
6. **Лучшая поддержка печати** - встроенный диалог печати
7. **Сигналы и слоты** - более удобная система обработки событий
8. **Лучше документированный** - больше примеров и туториалов

### Различия в архитектуре

#### Tkinter версия (старая)
```python
# Импорты разбросаны по модулям
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename

# Глобальное состояние
class TextEditor:
    def __init__(self):
        self.root = Tk()
        self.tab_manager = TabManager(self)
        # ... много параметров экземпляра
```

#### PyQt6 версия (новая)
```python
# Все импорты из PyQt6
from PyQt6.QtWidgets import QMainWindow, QTextEdit, QTabWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QIcon

# Правильная объектная архитектура
class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = QTabWidget()
        self.tab_data = {}
        # ... чистая структура
```

## 🔄 Основные изменения

### 1. Главное окно

**Tkinter:**
```python
self.root = Tk()
self.root.title("Редактор")
self.root.geometry('1200x700')
self.root.mainloop()
```

**PyQt6:**
```python
class TextEditorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Редактор")
        self.setGeometry(100, 100, 1200, 700)
        
    def run(self):
        app = QApplication(sys.argv)
        self.show()
        sys.exit(app.exec())
```

### 2. Вкладки

**Tkinter:**
```python
self.tab_control = ttk.Notebook(self.tab_frame)
self.tab_control.add(frame, text="Новый файл")
self.tab_control.bind("<<NotebookTabChanged>>", self.on_tab_changed)
```

**PyQt6:**
```python
self.tab_widget = QTabWidget()
self.tab_widget.tabCloseRequested.connect(self.close_tab)
self.tab_widget.currentChanged.connect(self.on_tab_changed)
self.tab_widget.addTab(text_edit, "Новый файл")
```

### 3. Текстовое редактирование

**Tkinter:**
```python
text_area = Text(frame, wrap='word', undo=True, font=('Arial', 11))
text_area.insert(1.0, content)
text_area.get(1.0, END)
text_area.bind('<KeyRelease>', lambda e: self.on_text_change())
```

**PyQt6:**
```python
text_edit = QTextEdit()
text_edit.setFont(QFont('Arial', 11))
text_edit.setPlainText(content)
text_edit.toPlainText()
text_edit.textChanged.connect(self.on_text_changed)
```

### 4. Диалоги файлов

**Tkinter:**
```python
from tkinter.filedialog import askopenfilename
file_path = askopenfilename(
    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
)
```

**PyQt6:**
```python
file_path, _ = QFileDialog.getOpenFileName(
    self,
    "Open File",
    "",
    "Text files (*.txt);;All files (*.*)"
)
```

### 5. Сообщения пользователю

**Tkinter:**
```python
from tkinter.messagebox import showinfo, askyesnocancel
showinfo("Title", "Message")
answer = askyesnocancel("Save", "Save changes?")
```

**PyQt6:**
```python
QMessageBox.information(self, "Title", "Message")
reply = QMessageBox.question(
    self, "Save", "Save changes?",
    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
)
```

### 6. Меню

**Tkinter:**
```python
menubar = Menu(self.root)
self.root.config(menu=menubar)
file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=self.open_file)
```

**PyQt6:**
```python
menubar = self.menuBar()
file_menu = menubar.addMenu("File")
file_menu.addAction("Open", self.open_file, QKeySequence.StandardKey.Open)
```

### 7. Горячие клавиши

**Tkinter:**
```python
self.root.bind('<Control-n>', lambda e: self.new_file())
self.root.bind('<Control-o>', lambda e: self.open_file())
```

**PyQt6:**
```python
QShortcut(QKeySequence.StandardKey.New, self, self.new_file)
QShortcut(QKeySequence.StandardKey.Open, self, self.open_file)
```

### 8. Панель инструментов

**Tkinter:**
```python
self.toolbar = Frame(self.root, bd=1, relief=RAISED)
self.toolbar.pack(side=TOP, fill=X)
Button(self.toolbar, text="New", command=self.new_file).pack(side=LEFT)
```

**PyQt6:**
```python
toolbar = self.addToolBar("Main Toolbar")
toolbar.addAction("New", self.new_file)
toolbar.addSeparator()
toolbar.addAction("Open", self.open_file)
```

### 9. Строка состояния

**Tkinter:**
```python
self.status_bar = Label(self.root, text="Ready", relief=SUNKEN)
self.status_bar.pack(side=BOTTOM, fill=X)
self.status_bar.config(text="New text")
```

**PyQt6:**
```python
self.statusBar().showMessage("Ready")
self.statusBar().showMessage("New text")
```

### 10. Таймер (для автосохранения)

**Tkinter:**
```python
self.editor.root.after(300000, self.autosave)
```

**PyQt6:**
```python
self.autosave_timer = QTimer()
self.autosave_timer.timeout.connect(self.autosave)
self.autosave_timer.start(300000)
```

## 📦 Структура проекта

```
Старая структура (Tkinter):
├── main.py
├── texteditor.py (~500 строк - смешанная логика)
├── core/
│   └── *.py (логика редактора)
├── features/
│   └── *.py (функции)
└── ui/
    └── *.py (интерфейс)

Новая структура (PyQt6):
├── main.py (~15 строк)
├── app/
│   ├── texteditor.py (~400 строк - чистая логика)
│   ├── core/
│   │   ├── file_manager.py
│   │   ├── editor_commands.py
│   │   └── session_manager.py
│   ├── features/
│   │   ├── search_replace.py
│   │   ├── autosave.py
│   │   └── theme_manager.py
│   ├── ui/
│   │   ├── menu.py
│   │   ├── toolbar.py
│   │   └── statusbar.py
│   └── utils/
│       └── constants.py
```

## 🎯 Новые возможности в PyQt6 версии

1. **Поддержка тем** - 4 встроенные темы (светлая, темная, синяя, Monokai)
2. **Лучший поиск** - с опциями (регистр, целые слова)
3. **Печать** - настоящий диалог печати вместо эмуляции
4. **Восстановление окна** - запоминание размеров и позиции
5. **Лучшая производительность** - быстрее открывает большие файлы
6. **Стилизация** - CSS-подобные стили для UI
7. **Системная интеграция** - использует нативные диалоги
8. **Лучшая поддержка высоких DPI** - правильно масштабируется

## 🔧 Миграция существующих проектов

Если вы хотите перенести свой существующий Tkinter проект на PyQt6:

1. **Переписать главное окно** - наследовать от QMainWindow
2. **Заменить виджеты** - Tkinter widgets → PyQt6 widgets
3. **Переделать обработку событий** - bind → connect
4. **Обновить диалоги** - QFileDialog, QMessageBox
5. **Переписать макет** - QVBoxLayout, QHBoxLayout вместо pack/grid
6. **Обновить меню** - menuBar().addMenu() вместо Menu()
7. **Тестировать** - убедиться, что все работает

## 📚 Ресурсы

- [PyQt6 Official Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [PyQt6 Tutorial](https://www.tutorialspoint.com/pyqt/)
- [Qt Design Patterns](https://doc.qt.io/qt-6/)

## ✅ Чек-лист миграции

- [ ] Создать новую структуру проекта
- [ ] Переписать главное окно
- [ ] Перенести все виджеты
- [ ] Обновить обработчики событий
- [ ] Переделать меню и панель инструментов
- [ ] Обновить диалоги файлов
- [ ] Проверить горячие клавиши
- [ ] Протестировать на разных платформах
- [ ] Обновить документацию
- [ ] Обновить requirements.txt

---

**PyQt6** - это современный выбор для разработки настольных приложений на Python! 🚀
