"""
Analysis Type Detail Object

"""


class AnalysisTypeDetail:
    def __init__(
        self,
        user: str,
        analysis_type_id: str,
        analysis_type_detail_type_id: int,
        analysis_type_detail_association_type_id: int,
        analysis_type_detail_label: str,
        analysis_type_titles_id=None
    ):
        self.user = user
        self.analysis_type_id = analysis_type_id
        self.analysis_type_detail_type_id = analysis_type_detail_type_id
        self.analysis_type_detail_association_type_id = analysis_type_detail_association_type_id
        self.analysis_type_detail_label = analysis_type_detail_label
        self.analysis_type_titles_id = analysis_type_titles_id


