"""
Base response used to standardize DB Results to defined AR API Responses
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Union


class BaseResponse(ABC):
    def __init__(self, response_data: Union[Dict, List[Dict]]):
        self.response = self._set_response(response_data=response_data)

    @abstractmethod
    def _set_response(self, response_data: Union[Dict, List[Dict]]): pass

    def get_response(self) -> any:
        """Get the ResponseObjects.  Keeping this as any right now since the FE is still expecting any kind of json"""
        return self.response



