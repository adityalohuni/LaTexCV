import yaml
from typing import Dict, List


class SectionManager:
    """Manage section objects, order and YAML persistence including
    commenting out hidden sections when saving.

    This manager operates on references passed in from the UI (sections dict
    and lists) so it can be introduced incrementally.
    """

    def __init__(self, model, sections: Dict[str, object], all_section_names: List[str], dynamic_sections: List[str]):
        self.model = model
        self.sections = sections
        self.all_section_names = all_section_names
        self.dynamic_sections = dynamic_sections

    def remove_section(self, section_name_or_obj):
        # Normalize
        if isinstance(section_name_or_obj, str):
            name = section_name_or_obj
        else:
            name = getattr(section_name_or_obj, 'section_name', None)
        if not name or name not in self.sections:
            return False

        # Remove widget and references
        sec = self.sections.pop(name, None)
        try:
            if getattr(sec, 'frame', None):
                sec.frame.destroy()
        except Exception:
            pass

        if name in self.all_section_names:
            try:
                self.all_section_names.remove(name)
            except Exception:
                pass
        if name in self.dynamic_sections:
            try:
                self.dynamic_sections.remove(name)
            except Exception:
                pass

        # Save updated order with commented hidden sections preserved
        try:
            self.autosave_order()
        except Exception:
            pass
        return True

    def reorder_section(self, section_name, new_index):
        if section_name not in self.all_section_names:
            return
        old_index = self.all_section_names.index(section_name)
        if old_index == new_index:
            return
        self.all_section_names.pop(old_index)
        self.all_section_names.insert(new_index, section_name)
        # Persist order
        try:
            self.autosave_order()
        except Exception:
            pass

    def autosave_order(self):
        """Write a YAML string where hidden (visible==False) sections are
        inserted as commented YAML blocks. The order key is always present.
        """
        # Build _order using current list
        order_block = yaml.dump({'_order': self.all_section_names}, default_flow_style=False)
        parts = [order_block.strip()]

        # For each section in order, dump its data; if the section exists and
        # is hidden, comment the block lines.
        for name in self.all_section_names:
            data = None
            sec = self.sections.get(name)
            if sec is not None:
                try:
                    data = sec.get_data()
                except Exception:
                    data = None
            else:
                # fallback to model-stored data
                try:
                    raw = self.model.get_data()
                    if isinstance(raw, dict):
                        data = raw.get(name)
                except Exception:
                    data = None

            block = yaml.dump({name: data}, default_flow_style=False).strip()
            if sec is not None and getattr(sec, 'visible', True) is False:
                # comment each line
                commented = '\n'.join('# ' + l for l in block.splitlines())
                parts.append(commented)
            else:
                parts.append(block)

        content = '\n\n'.join(parts) + '\n'

        # Write raw content to YAML file
        try:
            # Use model.save_raw if available, else fall back to save(dict)
            if hasattr(self.model, 'save_raw'):
                self.model.save_raw(content)
            else:
                # Fallback: parse back to dict for known visible sections
                self.model.save(yaml.safe_load(content))
        except Exception:
            # As a last resort, write directly to file path if model exposes yaml_file
            try:
                path = getattr(self.model, 'yaml_file', None)
                if path:
                    with open(path, 'w') as f:
                        f.write(content)
            except Exception:
                pass
