import yaml
from pathlib import Path

class ResumeModel:
    def __init__(self, yaml_file='resume.yaml'):
        self.yaml_file = yaml_file
        self.data = {}
        self.load()

    def load(self):
        if Path(self.yaml_file).exists():
            with open(self.yaml_file, 'r') as f:
                self.data = yaml.safe_load(f) or {}
        else:
            self.data = {}

    def save(self, data):
        self.data = data
        with open(self.yaml_file, 'w') as f:
            yaml.dump(self.data, f)

    def save_raw(self, raw_content: str):
        """Write raw YAML content (string) directly to the yaml file.

        This is used by SectionManager to preserve commented-out blocks.
        """
        with open(self.yaml_file, 'w') as f:
            f.write(raw_content)

    def get_data(self):
        # return a copy without internal _order key for UI convenience
        if isinstance(self.data, dict) and '_order' in self.data:
            d = dict(self.data)
            d.pop('_order', None)
            return d
        return self.data

    def get_order(self):
        if isinstance(self.data, dict):
            return self.data.get('_order')
        return None

    def set_data(self, data):
        self.data = data
