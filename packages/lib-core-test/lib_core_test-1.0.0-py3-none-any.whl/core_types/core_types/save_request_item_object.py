"""
Request Item Object Definition
Noting that we're making the MDTR items optional to reduce the blast radius of changes right now
"""
from typing import Dict, List
from iprm_api.save.types.field_group_detail_request_object import FieldGroupDetailRequestObject


# pylint: disable=too-many-arguments,too-many-instance-attributes
class SaveRequestItemObject:
    def __init__(
        self,
        gtm_id: int,
        analysis_type_detail_id: str,
        analysis_type_detail_name: str,
        analysis_type_detail_label: str,
        analysis_type_id: str,
        is_previously_saved: bool,
        rights_type_id: int,
        field_group_details_info: List[FieldGroupDetailRequestObject],
        tr_analysis_type_detail_id: str = None,
        tr_analysis_type_detail_label: str = None,
        dtr_analysis_type_detail_id: str = None,
        previously_saved: bool = False,
    ):
        self.gtm_id = gtm_id
        self.analysis_type_detail_id = analysis_type_detail_id
        self.analysis_type_detail_name = analysis_type_detail_name
        self.analysis_type_detail_label = analysis_type_detail_label
        self.analysis_type_id = analysis_type_id
        self.is_previously_saved = is_previously_saved
        self.rights_type_id = rights_type_id
        self.field_group_details_info = field_group_details_info
        self.tr_analysis_type_detail_id = tr_analysis_type_detail_id
        self.tr_analysis_type_detail_label = tr_analysis_type_detail_label
        self.dtr_analysis_type_detail_id = dtr_analysis_type_detail_id
        self.previously_saved = previously_saved

    def to_json(self) -> Dict:
        """Get object properties as json object"""
        return {
            "gtm_id": self.gtm_id,
            "analysis_type_detail_id": self.analysis_type_detail_id,
            "analysis_type_detail_name": self.analysis_type_detail_name,
            "analysis_type_detail_label": self.analysis_type_detail_label,
            "analysis_type_id": self.analysis_type_id,
            "is_previously_saved": self.is_previously_saved,
            "rights_type_id": self.rights_type_id,
            "field_group_details_info": [item.to_json() for item in self.field_group_details_info],
            "tr_analysis_type_detail_id": self.tr_analysis_type_detail_id,
            "tr_analysis_type_detail_id": self.tr_analysis_type_detail_id,
            "dtr_analysis_type_detail_id": self.dtr_analysis_type_detail_id,
            "previously_saved": self.previously_saved,
        }
