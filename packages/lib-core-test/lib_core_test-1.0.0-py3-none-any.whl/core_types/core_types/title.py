"""
Base Title Object
"""

class Title():
    def __init__(
        self,
        user: str,
        gtm_id: int,
        iprm_id: int,
        level_tag_desc: str,
        parent_iprm_id: int,
        parent_gtm_id: int,
        title_level: int
    ):
        self.user = user
        self.gtm_id = gtm_id
        self.iprm_id = iprm_id
        self.level_tag_desc = level_tag_desc
        self.parent_iprm_id = parent_iprm_id
        self.parent_gtm_id = parent_gtm_id
        self.title_level = title_level

