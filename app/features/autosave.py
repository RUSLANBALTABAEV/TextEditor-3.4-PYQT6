# app/autosave.py
"""
Менеджер автосохранения документов
"""
import time
from pathlib import Path
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QMessageBox
class AutoSaveManager:
    """Управление автосохранением"""
   
    def __init__(self, editor):
        self.editor = editor
        self.autosave_timer = QTimer()
        self.autosave_timer.timeout.connect(self.autosave)
       
    def toggle_autosave(self):
        """Включить/выключить автосохранение"""
        self.editor.auto_save_enabled = not self.editor.auto_save_enabled
       
        if self.editor.auto_save_enabled:
            self.start_autosave()
            QMessageBox.information(
                self.editor,
                "Автосохранение",
                "Автосохранение включено"
            )
        else:
            self.stop_autosave()
            QMessageBox.information(
                self.editor,
                "Автосохранение",
                "Автосохранение выключено"
            )
           
    def start_autosave(self):
        """Запустить автосохранение"""
        self.autosave_timer.start(self.editor.auto_save_interval)
       
    def stop_autosave(self):
        """Остановить автосохранение"""
        self.autosave_timer.stop()
       
    def autosave(self):
        """Выполнить автосохранение"""
        if not self.editor.auto_save_enabled:
            return
       
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data and tab_data.get('file_path') and tab_data.get('modified'):
                try:
                    file_path = tab_data['file_path']
                    content = tab_data['text_edit'].toPlainText()
                   
                    # Создаем резервную копию
                    backup_name = f"autosave_{Path(file_path).name}_{int(time.time())}.bak"
                    backup_path = self.editor.backup_dir / backup_name
                   
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                   
                    # Сохраняем основной файл
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                   
                    tab_data['modified'] = False
                   
                except Exception as e:
                    print(f"Ошибка автосохранения: {e}")
                   
    def set_autosave_interval(self, minutes):
        """Установить интервал автосохранения"""
        if minutes < 1:
            minutes = 1
       
        self.editor.auto_save_interval = minutes * 60000
       
        if self.editor.auto_save_enabled:
            self.stop_autosave()
            self.start_autosave()
