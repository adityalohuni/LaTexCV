import tkinter as tk
import ttkbootstrap as ttk
from .section_view import SectionView

class SummarySection(SectionView):
    def __init__(self, parent, data=None, **kwargs):
        super().__init__(parent, 'summary', **kwargs)
        self.widget = None
        self.create_widgets()
        if data:
            self.load_data(data)

    def create_widgets(self):
        self.widget = tk.Text(self.frame, height=3, wrap='word', font=("Courier New", 12))
        self.widget.pack(fill='x')

    def load_data(self, data):
        self.widget.delete('1.0', tk.END)
        self.widget.insert('1.0', data[0].get('description', '') if data else '')

    def get_data(self):
        return [{'description': self.widget.get('1.0', tk.END).strip()}]
