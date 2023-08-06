"""
Base request used to standardize Lambda events into a defined AR Request Object
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Union
from core_types.read_request_object import ReadRequestObject
from core_types.save_request_object import SaveRequestObject


class BaseRequest(ABC):
    def __init__(self, event: Union[Dict, List[Dict]]):
        self.path = event.get('path') if isinstance(event, Dict) else event[0].get('path')
        self.request = self._set_request(event=event)

    @abstractmethod
    def _set_request(self): pass

    def get_request(self) -> Union[ReadRequestObject, SaveRequestObject]:
        """Gets either the read or save request objects"""
        return self.request



