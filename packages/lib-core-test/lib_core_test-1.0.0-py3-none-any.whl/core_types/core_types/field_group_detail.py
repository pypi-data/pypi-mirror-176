"""
Field Group Detail Object
"""
from typing import List
from core_interfaces.i_field_group_detail_status import IFieldGroupDetailStatus


class FieldGroupDetail:
    def __init__(
        self,
        user: str,
        field_group_detail_id: str,
        field_group_detail_value: List[object],
        field_group_id: int,
        field_group_detail_status: IFieldGroupDetailStatus = None
    ):
        self.user = user
        self.field_group_detail_id = field_group_detail_id
        self.field_group_detail_value = field_group_detail_value
        self.field_group_id = field_group_id
        self.field_group_detail_status = field_group_detail_status

