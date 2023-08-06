"""
Save Request Object Definition
"""
from typing import List, Dict
from core_types.save_request_item_object import SaveRequestItemObject


# pylint: disable=too-many-arguments,too-many-instance-attributes
class SaveRequestObject:
    def __init__(
        self,
        event_path: str,
        user: int,
        rights_type_id: int,
        analysis_type_id: str,
        is_new_contract: bool,
        items: List[SaveRequestItemObject],
    ):
        self.event_path = event_path
        self.user = user
        self.rights_type_id = rights_type_id
        self.analysis_type_id = analysis_type_id
        self.is_new_contract = is_new_contract
        self.items = items

    def to_json(self) -> Dict:
        """Get object properties as json object"""
        return {
            "event_path": self.event_path,
            "user": self.user,
            "rights_type_id": self.rights_type_id,
            "analysis_type_id": self.analysis_type_id,
            "is_new_contract": self.is_new_contract,
            "items": [item.to_json() for item in self.items],
        }


"""
Save analysis
REQUEST OBJ {
user: "sso_id"
analysis_type_id: "123"
is_new_contract: true,
items: [
        {
            gtm_id = 99999
            analysis_type_detail_id = "000"
            analysis_type_detail_name = "CONTRACT_INFO"
            analysis_type_detail_label = "Contract Info"
            analysis_type_id = "123"
            is_previously_saved = false
            field_group_details_info = [
                {
                    field_group_detail_id = "999"
                    field_group_id = 100004
                    field_group_status_id = 1
                    field_group_status_note = {}
                    fields = []
                    }
            ]
        },
        {
            gtm_id = 99999
            analysis_type_detail_id = "111"
            analysis_type_detail_name = "TITLE_RIGHTS"
            analysis_type_detail_label = "Title Rights 1"
            analysis_type_id = "123"
            is_previously_saved = false
            field_group_details_info = [
                {
                    field_group_detail_id = "888"
                    field_group_id = 110115
                    field_group_status_id = 1
                    field_group_status_note = {}
                    fields = []
                }
            ]
        }
    ]  
}     
==================================================
SAVE STATUS 
REQUEST OBJ {
user: "sso_id"
analysis_type_id: "456"
is_new_contract: false,
items: [
        {
            gtm_id = 344650
            analysis_type_detail_id = "111"
            analysis_type_detail_name = "CONTRACT_INFO"
            analysis_type_detail_label = "Contract Info"
            analysis_type_id = ""
            is_previously_saved = null
            field_group_details_info = [
                {
                    field_group_detail_id = ""
                    field_group_id = 110011
                    field_group_status_id = 1
                    field_group_status_note = { "note": "" }
                    fields = []
                }
            ]
        },
        {
            gtm_id = 99999
            analysis_type_detail_id = "111"
            analysis_type_detail_name = "TITLE_RIGHTS"
            analysis_type_detail_label = "Title Rights 1"
            analysis_type_id = "123"
            is_previously_saved = null
            field_group_details_info = [
                {
                    field_group_detail_id = ""
                    field_group_id = 110011
                    field_group_status_id = 1
                    field_group_status_note = { "note": "" }
                    fields = []
                }
            ]
        }
    ]  
}     
=================================
SAVE ASSOCIATED NO DTR
REQUEST OBJ {
user: "sso_id"
analysis_type_id: "789"
is_new_contract: false,
items: [
        {
            gtm_id = 375187
            analysis_type_detail_id = null
            analysis_type_detail_name = ""
            analysis_type_detail_label = ""
            analysis_type_id = "789"
            is_previously_saved = null
            field_group_details_info = []
        },
        {
            gtm_id = 432288
            analysis_type_detail_id = null
            analysis_type_detail_name = ""
            analysis_type_detail_label = ""
            analysis_type_id = "789"
            is_previously_saved = null
            field_group_details_info = []
        }
    ]  
}   


=================================
SAVE ASSOCIATED DTR
REQUEST OBJ {
user: "sso_id"
analysis_type_id: "101"
is_new_contract: false,
items: [
        {
            gtm_id = 375187
            analysis_type_detail_id = "555"
            analysis_type_detail_name = "DEFAULT_TITLE_RIGHTS"
            analysis_type_detail_label = ""
            analysis_type_id = "101"
            is_previously_saved = null
            field_group_details_info = []
        },
        {
            gtm_id = 432288
            analysis_type_detail_id = 555
            analysis_type_detail_name = "DEFAULT_TITLE_RIGHTS"
            analysis_type_detail_label = ""
            analysis_type_id = "789"
            is_previously_saved = null
            field_group_details_info = []
        }
    ]  
}

=================================
SAVE DUPLICATE DTR
REQUEST OBJ {
user: "sso_id"
analysis_type_id: "ddd280b5-684e-5671-a8de-5f3e951f03ad"
is_new_contract: false,
items: [{
            gtm_id = None
            analysis_type_detail_id = "c190632a-8455-efe5-1a7c-10b0d4b7674f"
            analysis_type_detail_name = "DEFAULT_TITLE_RIGHTS"
            analysis_type_detail_label = "Default Title Rights 2"
            analysis_type_id = "ddd280b5-684e-5671-a8de-5f3e951f03ad"
            is_previously_saved = false
            field_group_details_info = []
        },
        {
            gtm_id = None
            analysis_type_detail_id = "92b685c4-2751-6ef9-3584-d09bc86eaeea"
            analysis_type_detail_name = "DEFAULT_TITLE_RIGHTS"
            analysis_type_detail_label = ""
            analysis_type_id = "ddd280b5-684e-5671-a8de-5f3e951f03ad"
            is_previously_saved = false
            field_group_details_info = []
        }]
}
"""
