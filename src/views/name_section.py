import tkinter as tk
import ttkbootstrap as ttk
from .section_view import SectionView

class NameSection(SectionView):
    def __init__(self, parent, data=None):
        super().__init__(parent, 'name')
        self.widgets = {}
        self.create_widgets()
        if data:
            self.load_data(data)

    def create_widgets(self):
        ttk.Label(self.frame, text='First Name:').pack(anchor='w')
        first_entry = tk.Text(self.frame, height=1, wrap='word', font=("Courier New", 12))
        first_entry.pack(fill='x')
        self.widgets['first'] = first_entry
        ttk.Label(self.frame, text='Last Name:').pack(anchor='w')
        last_entry = tk.Text(self.frame, height=1, wrap='word', font=("Courier New", 12))
        last_entry.pack(fill='x')
        self.widgets['last'] = last_entry

    def load_data(self, data):
        self.widgets['first'].delete('1.0', tk.END)
        self.widgets['first'].insert('1.0', data.get('first', ''))
        self.widgets['last'].delete('1.0', tk.END)
        self.widgets['last'].insert('1.0', data.get('last', ''))

    def get_data(self):
        return {
            'first': self.widgets['first'].get('1.0', 'end-1c'),
            'last': self.widgets['last'].get('1.0', 'end-1c')
        }
