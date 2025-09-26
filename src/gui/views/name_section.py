import tkinter as tk

import ttkbootstrap as ttk

from gui.fonts import FONTS

from .section_view import SectionView


class NameSection(SectionView):
    def __init__(self, parent, data=None):
        super().__init__(parent, "name")
        self.widgets = {}
        self.create_widgets()
        if data:
            self.load_data(data)

    def create_widgets(self):
        ttk.Label(self.frame, text="First Name:", font=FONTS["text"]).pack(
            anchor="w", pady=(5, 0)
        )
        first_entry = ttk.Entry(self.frame, font=FONTS["text"])
        first_entry.pack(fill="x", pady=(0, 10))
        self.widgets["first"] = first_entry
        ttk.Label(self.frame, text="Last Name:", font=FONTS["text"]).pack(
            anchor="w", pady=(5, 0)
        )
        last_entry = ttk.Entry(self.frame, font=FONTS["text"])
        last_entry.pack(fill="x", pady=(0, 10))
        self.widgets["last"] = last_entry

    def load_data(self, data):
        self.widgets["first"].delete(0, tk.END)
        self.widgets["first"].insert(0, data.get("first", ""))
        self.widgets["last"].delete(0, tk.END)
        self.widgets["last"].insert(0, data.get("last", ""))

    def get_data(self):
        return {
            "first": self.widgets["first"].get(),
            "last": self.widgets["last"].get(),
        }
