import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkfontawesome import icon_to_image


class SectionView:
    def __init__(self, parent, section_name, visible=True):
        self.parent = parent
        self.section_name = section_name
        self.visible = visible
        self.frame = None
        self.eye_button = None
        self.items = []
        self.create_frame()

    def create_frame(self):
        self.frame = ttk.Frame(self.parent)
        if self.visible:
            self.frame.pack(fill='x', pady=5)
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill='x')
        label = ttk.Label(header_frame, text=self.section_name.replace('_', ' ').title(), font=("Arial", 14, "bold"))
        label.pack(side='left')
        self.eye_button = ttk.Button(header_frame, image=icon_to_image('fa-eye') if self.visible else icon_to_image('fa-eye-splash'), command=self.toggle_visibility, bootstyle=(LINK, "secondary"))
        self.eye_button.pack(side='right')

    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.frame.pack(fill='x', pady=5)
            self.eye_button.config(image=icon_to_image('fa-eye'))
        else:
            self.frame.pack_forget()
            self.eye_button.config(image=icon_to_image('fa-eye-slash'))

    def add_meta(self, item_frame, item_dict, current_row):
        if item_dict is None:
            return
        row = current_row + len(item_dict['meta_entries']) + 1
        key_entry = tk.Text(item_frame, height=1, wrap='word', width=8, font=("Courier New", 12))
        key_entry.grid(row=row, column=0, sticky='w', padx=(5,5))
        value_entry = tk.Text(item_frame, height=1, wrap='word', width=25, font=("Courier New", 12))
        value_entry.grid(row=row, column=1, sticky='ew', padx=(0,5))
        remove_meta_btn = ttk.Button(item_frame, text='X', command=lambda: self.remove_meta(item_frame, item_dict, key_entry, value_entry), bootstyle=DANGER)
        remove_meta_btn.grid(row=row, column=2, sticky='e', padx=(0,5))
        item_dict['meta_entries'].append({'key': key_entry, 'value': value_entry})
        self.update_remove_button_rowspan(item_frame)

    def remove_meta(self, item_frame, item_dict, key_entry, value_entry):
        key_entry.destroy()
        value_entry.destroy()
        item_dict['meta_entries'] = [e for e in item_dict['meta_entries'] if not (e['key'] is key_entry and e['value'] is value_entry)]
        self.update_remove_button_rowspan(item_frame)

    def update_remove_button_rowspan(self, item_frame):
        for child in item_frame.winfo_children():
            if isinstance(child, ttk.Button) and child.cget('text') == 'Remove':
                max_row = 0
                for c in item_frame.winfo_children():
                    info = c.grid_info()
                    if 'row' in info:
                        max_row = max(max_row, int(info['row']))
                child.grid(rowspan=max_row + 1)
                break

    def remove_item(self, frame, item_dict):
        frame.destroy()
        self.items.remove(item_dict)
