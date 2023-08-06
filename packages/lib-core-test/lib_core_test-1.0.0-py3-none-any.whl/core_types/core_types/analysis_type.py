"""
Analysis Type Object
"""


class AnalysisType:
    def __init__(
        self,
        user: str,
        analysis_type_id: str,
        analysis_category_id: int,
        rights_type_id: int,
        ar_contract_number: str = None
    ):
        self.user = user
        self.analysis_type_id = analysis_type_id
        self.analysis_category_id = analysis_category_id
        self.rights_type_id = rights_type_id
        self.ar_contract_number = ar_contract_number
