"""Base class for CV section views."""

import ttkbootstrap as ttk
from ttkbootstrap.constants import DANGER, LINK

from gui.fonts import FONTS


class SectionView:
    """Base view class for CV sections."""

    def __init__(self, parent, section_name, visible=True):
        """Initialize the section view."""
        self.parent = parent
        self.section_name = section_name
        self.visible = visible
        self.frame = None
        self.eye_button = None
        self.items = []
        self.create_frame()

    def create_frame(self):
        """Create the frame for the section."""
        self.frame = ttk.Frame(
            self.parent, borderwidth=1, relief="solid", padding=10
        )  # Added border and padding for card-like appearance
        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.pack(fill="x", pady=(0, 10))  # Added pady
        label = ttk.Label(
            self.header_frame,
            text=self.section_name.replace("_", " ").title(),
            font=FONTS["subheader"],
        )
        label.pack(side="left")
        self.eye_button = ttk.Button(
            self.header_frame,
            text="Visible" if self.visible else "Hidden",
            command=self.toggle_visibility,
            width=10,
            height=2,
        )
        self.eye_button.pack(side="right")

    def toggle_visibility(self):
        """Toggle the visibility of the section."""
        self.visible = not self.visible
        self.eye_button.config(text="Visible" if self.visible else "Hidden")
        self.frame.master.master.master.show_current_section()

    def add_meta(self, item_frame, item_dict, current_row):
        """Add a meta field to an item."""
        if item_dict is None:
            return
        row = current_row + len(item_dict["meta_entries"]) + 1
        key_entry = ttk.Entry(item_frame, font=FONTS["mono"], width=10)
        key_entry.grid(row=row, column=0, sticky="w", padx=(5, 5))
        value_entry = ttk.Entry(item_frame, font=FONTS["mono"])
        value_entry.grid(row=row, column=1, sticky="ew", padx=(0, 5))
        remove_meta_btn = ttk.Button(
            item_frame,
            text="X",
            command=lambda: self.remove_meta(
                item_frame, item_dict, key_entry, value_entry
            ),
            bootstyle=DANGER,
        )
        remove_meta_btn.grid(row=row, column=2, sticky="e", padx=(0, 5))
        item_dict["meta_entries"].append({"key": key_entry, "value": value_entry})
        self.update_remove_button_rowspan(item_frame)

    def remove_meta(self, item_frame, item_dict, key_entry, value_entry):
        """Remove a meta field from an item."""
        key_entry.destroy()
        value_entry.destroy()
        item_dict["meta_entries"] = [
            e
            for e in item_dict["meta_entries"]
            if not (e["key"] is key_entry and e["value"] is value_entry)
        ]
        self.update_remove_button_rowspan(item_frame)

    def update_remove_button_rowspan(self, item_frame):
        """Update the rowspan of the remove button."""
        for child in item_frame.winfo_children():
            if isinstance(child, ttk.Button) and child.cget("text") == "Remove":
                max_row = 0
                for c in item_frame.winfo_children():
                    info = c.grid_info()
                    if "row" in info:
                        max_row = max(max_row, int(info["row"]))
                child.grid(rowspan=max_row + 1)
                break

    def remove_item(self, frame, item_dict):
        """Remove an item from the section."""
        frame.destroy()
        self.items.remove(item_dict)
