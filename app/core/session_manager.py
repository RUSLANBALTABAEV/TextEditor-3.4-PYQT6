"""
Менеджер сессий - сохранение и восстановление состояния редактора
"""
import json
from pathlib import Path


class SessionManager:
    """Управление сессиями пользователя"""
    
    def __init__(self, editor):
        self.editor = editor
        
    def save_session(self):
        """Сохранение текущей сессии"""
        session_data = {
            'tabs': [],
            'theme': self.editor.theme,
            'auto_save_enabled': self.editor.auto_save_enabled,
            'auto_save_interval': self.editor.auto_save_interval
        }
        
        for i in range(self.editor.tab_widget.count()):
            tab_data = self.editor.get_tab_data(i)
            if tab_data:
                tab_info = {
                    'file_path': tab_data['file_path'],
                    'content': tab_data['text_edit'].toPlainText(),
                    'name': tab_data['name']
                }
                session_data['tabs'].append(tab_info)
        
        try:
            with open(self.editor.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения сессии: {e}")
            
    def load_session(self):
        """Загрузка сохраненной сессии"""
        try:
            if self.editor.session_file.exists():
                with open(self.editor.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Восстанавливаем настройки
                self.editor.theme = session_data.get('theme', 'light')
                self.editor.auto_save_enabled = session_data.get('auto_save_enabled', False)
                self.editor.auto_save_interval = session_data.get('auto_save_interval', 300000)
                
                # Очищаем пустую первую вкладку
                if self.editor.tab_widget.count() == 1:
                    self.editor.tab_widget.removeTab(0)
                
                # Восстанавливаем вкладки
                for tab_info in session_data.get('tabs', []):
                    self.editor.new_tab(
                        tab_info.get('file_path'),
                        tab_info.get('content')
                    )
                
                # Если нет вкладок, создаем пустую
                if self.editor.tab_widget.count() == 0:
                    self.editor.new_tab()
                    
        except Exception as e:
            print(f"Ошибка загрузки сессии: {e}")
