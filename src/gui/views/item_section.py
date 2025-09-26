"""Item section view for CV sections with multiple items."""

import tkinter as tk

import ttkbootstrap as ttk
from ttkbootstrap.constants import DANGER, INFO, SUCCESS

from gui.fonts import FONTS

from .section_view import SectionView


class ItemSection(SectionView):
    """View for sections that contain multiple items."""

    def __init__(self, parent, section_name, fields, data=None):
        """Initialize the item section."""
        super().__init__(parent, section_name)
        self.fields = (
            fields  # list of field names, e.g., ['institution', 'degree', ...]
        )
        self.left = True
        self.left_button = ttk.Button(
            self.header_frame,
            text="Left",
            command=self.toggle_left,
            width=6,
            height=2,
        )
        self.left_button.pack(side="right", padx=(5, 0))
        self.container = ttk.Frame(self.frame)
        self.container.pack(fill="x")
        self.add_button = ttk.Button(
            self.frame,
            text=f"Add {section_name.title()}",
            command=self.add_item,
            bootstyle=SUCCESS,
        )
        self.add_button.pack(anchor="w", pady=(5, 10))
        if data:
            self.load_data(data)

    def add_item(self):
        """Add a new item to the section."""
        item_frame = ttk.Frame(
            self.container, borderwidth=1, relief="solid", padding=5
        )  # Added padding
        item_frame.pack(fill="x", pady=5)  # Increased pady
        item_frame.grid_columnconfigure(0, weight=0)
        item_frame.grid_columnconfigure(1, weight=1)
        item_frame.grid_columnconfigure(2, weight=0)
        widgets = {}
        row = 0
        for field in self.fields:
            ttk.Label(
                item_frame, text=field.capitalize() + ":", font=FONTS["text"]
            ).grid(row=row, column=0, sticky="w", padx=(5, 5), pady=(5, 0))
            if field == "description":
                widget = tk.Text(item_frame, height=2, wrap="word", font=FONTS["text"])
            else:
                widget = ttk.Entry(item_frame, font=FONTS["text"])
            widget.grid(row=row, column=1, sticky="ew", padx=(0, 5), pady=(0, 5))
            widgets[field] = widget
            row += 1
        widgets["frame"] = item_frame
        widgets["meta_entries"] = []
        add_meta_btn = ttk.Button(
            item_frame,
            text="Add Meta",
            command=lambda: self.add_meta(item_frame, widgets, row - 1),
            bootstyle=INFO,
        )
        add_meta_btn.grid(row=row - 1, column=2, sticky="ne", padx=(0, 5))
        remove_btn = ttk.Button(
            item_frame,
            text="Remove",
            command=lambda: self.remove_item(item_frame, widgets),
            bootstyle=DANGER,
        )
        remove_btn.grid(row=0, column=2, rowspan=row, sticky="ne", padx=(0, 5))
        self.items.append(widgets)

    def load_data(self, data):
        """Load data into the section."""
        for item_data in data:
            self.add_item()
            last = self.items[-1]
            for field in self.fields:
                if field == "description":
                    last[field].delete("1.0", tk.END)
                    last[field].insert("1.0", item_data.get(field, ""))
                else:
                    last[field].delete(0, tk.END)
                    last[field].insert(0, item_data.get(field, ""))
            for k, v in item_data.items():
                if k not in self.fields and k != "left":
                    self.add_meta(
                        last["frame"] if "frame" in last else None,
                        last,
                        len(self.fields) - 1,
                    )
                    meta_last = last["meta_entries"][-1]
                    meta_last["key"].delete(0, tk.END)
                    meta_last["key"].insert(0, k)
                    meta_last["value"].delete(0, tk.END)
                    meta_last["value"].insert(0, str(v))
        if data:
            self.left = data[0].get("left", True)
            self.left_button.config(text="Left" if self.left else "Right")

    def toggle_left(self):
        """Toggle the left alignment."""
        self.left = not self.left
        self.left_button.config(text="Left" if self.left else "Right")

    def get_data(self):
        """Get the data from the section."""
        result = []
        for item in self.items:
            data = {
                field: (
                    item[field].get("1.0", tk.END).strip()
                    if field == "description"
                    else item[field].get()
                )
                for field in self.fields
            }
            data.update(
                {e["key"].get(): e["value"].get() for e in item["meta_entries"]}
            )
            data["left"] = self.left
            result.append(data)
        return result
