import tkinter as tk
import ttkbootstrap as ttk
from .section_view import SectionView

class ContactSection(SectionView):
    def __init__(self, parent, data=None, **kwargs):
        super().__init__(parent, 'contact', **kwargs)
        self.widgets = {}
        self.create_widgets()
        if data:
            self.load_data(data)

    def create_widgets(self):
        for key in ['email', 'portfolio', 'github', 'linkedin']:
            ttk.Label(self.frame, text=key.capitalize() + ':').pack(anchor='w')
            entry = tk.Text(self.frame, height=1, wrap='word', font=("Courier New", 12))
            entry.pack(fill='x')
            self.widgets[key] = entry

    def load_data(self, data):
        for key in ['email', 'portfolio', 'github', 'linkedin']:
            self.widgets[key].delete('1.0', tk.END)
            self.widgets[key].insert('1.0', data.get(key, ''))

    def get_data(self):
        return {key: self.widgets[key].get('1.0', 'end-1c') for key in ['email', 'portfolio', 'github', 'linkedin']}
