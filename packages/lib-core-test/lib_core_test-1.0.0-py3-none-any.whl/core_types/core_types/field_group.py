"""
Field Group Object
"""


class FieldGroup():
    def __init__(
            self,
            user: str,
            field_group_id: int,
            category_id: int,
            field_group_data: object,  # standardized field group data?
            field_group_display_name: str
    ):
        self.user = user
        self.field_group_id = field_group_id
        self.category_id = category_id
        self.field_group_data = field_group_data
        self.field_group_display_name = field_group_display_name
