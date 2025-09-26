from .item_section import ItemSection


class EducationSection(ItemSection):
    def __init__(self, parent, data=None):
        fields = ["institution", "degree", "location", "dates", "description"]
        super().__init__(parent, "education", fields, data)
