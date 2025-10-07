from .item_section import ItemSection

class SkillsSection(ItemSection):
    def __init__(self, parent, data=None, **kwargs):
        fields = ['title', 'description']
        super().__init__(parent, 'skills', fields, data, **kwargs)

    def get_data(self):
        data = super().get_data()
        for item in data:
            item['left'] = True
        return data
