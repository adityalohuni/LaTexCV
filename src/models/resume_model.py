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

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
