import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from .section_view import SectionView

class InterestsSection(SectionView):
    def __init__(self, parent, data=None, **kwargs):
        super().__init__(parent, 'interests', **kwargs)
        self.container = ttk.Frame(self.frame)
        self.container.pack(fill='x')
        self.add_button = ttk.Button(self.frame, text='Add Interest', command=self.add_item, bootstyle=SUCCESS)
        self.add_button.pack(anchor='w', pady=(5,10))
        if data:
            self.load_data(data)

    def add_item(self):
        item_frame = ttk.Frame(self.container, borderwidth=1, relief='solid')
        item_frame.pack(fill='x', pady=2)
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=0)
        interest_entry = tk.Text(item_frame, height=1, wrap='word', width=25, font=("Courier New", 12))
        interest_entry.grid(row=0, column=0, sticky='ew', padx=(5,5))
        remove_btn = ttk.Button(item_frame, text='Remove', command=lambda: self.remove_item(item_frame, {'frame': item_frame, 'interest': interest_entry}), bootstyle=DANGER)
        remove_btn.grid(row=0, column=1, sticky='e', padx=(0,5))
        self.items.append({'frame': item_frame, 'interest': interest_entry})

    def load_data(self, data):
        for item in data:
            if isinstance(item, str):
                self.add_item()
                last = self.items[-1]
                last['interest'].delete('1.0', tk.END)
                last['interest'].insert('1.0', item)

    def get_data(self):
        return [{'left': True}] + [item['interest'].get('1.0', 'end-1c') for item in self.items]
