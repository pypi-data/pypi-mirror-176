"""
Field Group Detail Status Interface

TODO
"""
from abc import ABC, abstractmethod


class IFieldGroupDetailStatus(ABC):

    @abstractmethod
    def set_status(self): pass

    @abstractmethod
    def get_status(self): pass
