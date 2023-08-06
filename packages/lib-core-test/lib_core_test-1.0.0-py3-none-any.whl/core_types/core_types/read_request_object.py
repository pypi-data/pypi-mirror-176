"""
Request Object 
"""


class ReadRequestObject:
    def __init__(
        self,
        requester: str,
        request_data: any
    ):
        self.requester = requester
        self.request_data = request_data

    def get_requester(self) -> str:
        return self.requester

    def get_request_data(self) -> any:
        return self.request_data
