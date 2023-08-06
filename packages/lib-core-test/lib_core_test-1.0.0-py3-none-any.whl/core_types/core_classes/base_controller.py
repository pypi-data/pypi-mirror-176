"""
Base controller to be extended in any AR Lambda
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Union
from core_types.read_request_object import ReadRequestObject
from core_types.save_request_object import SaveRequestItemObject
from core_types.response_object import ResponseObject
from abc import ABC, abstractmethod


class BaseController(ABC):

    @abstractmethod
    def _process_request(self, event: Dict) -> Union[List[SaveRequestItemObject], List[ReadRequestObject]]:
        """ Sets incoming Lambda event to IPRM's Request Object """
    
    @abstractmethod
    def _interact_with_database(self, request: Union[List[SaveRequestItemObject], List[ReadRequestObject]]) -> any:
        """ Performs necessary database interactions from the lambda request """

    @abstractmethod
    def _format_response(self, db_result: any) -> List[ResponseObject]:
        """ Transforms results returned from database to standardized IPRM's Response Object"""

    def execute(self, event) -> List[ResponseObject]:
        """ Public method called from any lambda handler """
        try:
            request = self._process_request(event=event)
            db_result = self._interact_with_database(request=request)
            return self._format_response(db_result=db_result)
        except Exception:
            # LOGGER.exception(f"Lambda Controller Error on {event}")
            raise
