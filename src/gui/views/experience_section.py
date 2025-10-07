from .item_section import ItemSection


class ExperienceSection(ItemSection):
    def __init__(self, parent, data=None, **kwargs):
        fields = ["company", "title", "location", "dates", "description"]
        super().__init__(parent, "experience", fields, data, **kwargs)

    def get_data(self):
        data = super().get_data()
        # for item in data:
            # item["left"] = True
        return data
