import tkinter as tk

import ttkbootstrap as ttk

from gui.fonts import FONTS

from .section_view import SectionView


class ContactSection(SectionView):
    def __init__(self, parent, data=None):
        super().__init__(parent, "contact")
        self.widgets = {}
        self.create_widgets()
        if data:
            self.load_data(data)

    def create_widgets(self):
        for key in ["email", "portfolio", "github", "linkedin"]:
            ttk.Label(self.frame, text=key.capitalize() + ":", font=FONTS["text"]).pack(
                anchor="w", pady=(5, 0)
            )
            entry = ttk.Entry(self.frame, font=FONTS["text"])
            entry.pack(fill="x", pady=(0, 10))
            self.widgets[key] = entry

    def load_data(self, data):
        for key in ["email", "portfolio", "github", "linkedin"]:
            self.widgets[key].delete(0, tk.END)
            self.widgets[key].insert(0, data.get(key, ""))

    def get_data(self):
        return {
            key: self.widgets[key].get()
            for key in ["email", "portfolio", "github", "linkedin"]
        }
