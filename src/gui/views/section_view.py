import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkfontawesome import icon_to_image


class SectionView:
    def __init__(self, parent, section_name, visible=True, drag_callback=None,
                 move_up_callback=None, move_down_callback=None,
                 remove_callback=None, visibility_callback=None):
        self.parent = parent
        self.section_name = section_name
        self.visible = visible
        self.frame = None
        self.eye_button = None
        self.items = []

        # Optional callbacks provided by the container (MainWindow)
        # drag_callback(action, section_name, event) where action is 'start','motion','end'
        self.drag_callback = drag_callback
        self.move_up_callback = move_up_callback
        self.move_down_callback = move_down_callback
        # Optional callback to request the container remove this section.
        # Signature assumption: remove_callback(section_name) -> False to cancel, otherwise proceed.
        self.remove_callback = remove_callback
        # Optional callback to notify container/manager of visibility change
        self.visibility_callback = visibility_callback

        self.create_frame()

    def create_frame(self):
        self.frame = ttk.Frame(self.parent)
        # Always pack the frame in the editor; visibility now controls enabled/muted state
        self.frame.pack(fill='x', pady=5)

        # Header holds the title, drag handle, move buttons and visibility toggle.
        self.header_frame = ttk.Frame(self.frame)
        self.header_frame.pack(fill='x')

        # Drag handle (user can click and drag this to reorder sections)
        drag_handle = ttk.Label(self.header_frame, text='☰', font=("Arial", 14))
        drag_handle.pack(side='left', padx=(0, 8))
        # show move cursor when hovering drag handle
        try:
            drag_handle.configure(cursor='fleur')
        except Exception:
            pass
        # Bind drag events to the handle; callbacks are no-ops if not provided
        if self.drag_callback:
            drag_handle.bind('<ButtonPress-1>', lambda e: self.drag_callback('start', self.section_name, e))
            drag_handle.bind('<B1-Motion>', lambda e: self.drag_callback('motion', self.section_name, e))
            drag_handle.bind('<ButtonRelease-1>', lambda e: self.drag_callback('end', self.section_name, e))

        # Section title
        label = ttk.Label(self.header_frame, text=self.section_name.replace('_', ' ').title(), font=("Arial", 14, "bold"))
        label.pack(side='left')

        # Optional move up/down buttons for accessibility (keyboard users)
        if self.move_up_callback:
            up_btn = ttk.Button(self.header_frame, text='↑', width=3,
                                command=lambda: self.move_up_callback(self.section_name),
                                bootstyle=(LINK, "secondary"))
            up_btn.pack(side='right', padx=(4, 0))
        if self.move_down_callback:
            down_btn = ttk.Button(self.header_frame, text='↓', width=3,
                                  command=lambda: self.move_down_callback(self.section_name),
                                  bootstyle=(LINK, "secondary"))
            down_btn.pack(side='right')

        # Remove section button (danger style)
        remove_btn = ttk.Button(self.header_frame, text='Remove', width=8,
                                command=self.remove_section, bootstyle=DANGER)
        remove_btn.pack(side='right', padx=(4, 0))

        # Small visibility toggle: show a compact eye glyph and change bootstyle
        # to a gray style when hidden. Visibility is not stored in YAML; hiding
        # simply mutes the section in the UI; the manager will comment it out.
        eye_text = '👁'
        eye_boot = 'info' if self.visible else 'secondary'
        # small width so it doesn't dominate header
        self.eye_button = ttk.Button(
            self.header_frame,
            text=eye_text,
            width=3,
            command=self.toggle_visibility,
            bootstyle=eye_boot,
        )
        self.eye_button.pack(side='right', padx=(6, 0))

        # Ensure initial enabled/disabled state matches self.visible
        try:
            self.set_enabled(self.visible)
        except Exception:
            pass

    def set_enabled(self, enabled: bool):
        """Enable or disable all interactive widgets inside this section and
        apply a muted appearance when disabled."""
        def walk(widget):
            # never disable header controls (so the toggle remains clickable)
            try:
                if hasattr(self, 'header_frame') and widget is self.header_frame:
                    return
            except Exception:
                pass
            # apply to this widget
            try:
                # Text widgets (tk.Text)
                if isinstance(widget, tk.Text):
                    widget.config(state='normal' if enabled else 'disabled')
                # tk.Entry
                elif isinstance(widget, tk.Entry):
                    widget.config(state='normal' if enabled else 'disabled')
                else:
                    # ttk widgets support state() API
                    try:
                        if enabled:
                            widget.state(["!disabled"])
                        else:
                            widget.state(["disabled"])
                    except Exception:
                        pass
            except Exception:
                pass
            # recurse
            for c in widget.winfo_children():
                walk(c)
        walk(self.frame)

    def toggle_visibility(self):
        self.visible = not self.visible
        # Do not remove the frame from layout; only enable/disable its widgets
        try:
            self.set_enabled(self.visible)
        except Exception:
            pass
        # Notify container/manager so YAML can be updated (comment/uncomment)
        try:
            if self.visibility_callback:
                # visibility_callback is expected to be a no-arg callable
                try:
                    self.visibility_callback()
                except TypeError:
                    # fallback: try passing section_name
                    try:
                        self.visibility_callback(self.section_name)
                    except Exception:
                        pass
        except Exception:
            pass
        # Update eye button appearance
        try:
            if self.visible:
                self.eye_button.config(bootstyle='info', text='👁')
            else:
                self.eye_button.config(bootstyle='secondary', text='👁')
        except Exception:
            # Fallback text-only label adjustments
            try:
                self.eye_button.config(text='👁' if self.visible else '👁')
            except Exception:
                pass

    def add_meta(self, item_frame, item_dict, current_row):
        if item_dict is None:
            return
        row = current_row + len(item_dict['meta_entries']) + 1
        # Use single-line Entry widgets for meta key/value for more predictable saving
        key_entry = tk.Entry(item_frame, width=12, font=("Courier New", 12))
        key_entry.grid(row=row, column=0, sticky='w', padx=(5,5))
        value_entry = tk.Entry(item_frame, width=30, font=("Courier New", 12))
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

    def remove_section(self):
        """Request removal of this entire section.

        If a container-provided callback exists, call it with the section name.
        If the callback returns False, cancel the removal. Otherwise destroy the
        section frame locally.
        """
        try:
            if self.remove_callback:
                try:
                    res = self.remove_callback(self.section_name)
                except TypeError:
                    # Fallback if callback expects different signature
                    res = self.remove_callback(self)
                # If callback explicitly returned False, do not remove locally
                if res is False:
                    return
        except Exception:
            # Ignore errors from callback and continue to remove locally
            pass

        try:
            if self.frame:
                self.frame.destroy()
        except Exception:
            pass
