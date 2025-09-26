import yaml
from pathlib import Path

class YAMLHandler:
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path

    def load(self):
        if Path(self.yaml_path).exists():
            with open(self.yaml_path, 'r') as f:
                return f.read()
        return ''

    def save(self, content):
        yaml.safe_load(content)  # Validate YAML
        with open(self.yaml_path, 'w') as f:
            f.write(content)

    def load_dict(self):
        if Path(self.yaml_path).exists():
            with open(self.yaml_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
