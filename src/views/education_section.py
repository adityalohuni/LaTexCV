from .item_section import ItemSection

class EducationSection(ItemSection):
    def __init__(self, parent, data=None):
        fields = ['institution', 'degree', 'location', 'dates', 'description']
        super().__init__(parent, 'education', fields, data)

    def get_data(self):
        data = super().get_data()
        for item in data:
            item['left'] = True
        return data
