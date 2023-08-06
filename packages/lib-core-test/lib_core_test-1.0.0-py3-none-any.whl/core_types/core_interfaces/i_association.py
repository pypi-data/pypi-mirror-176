"""
Association Interface

TODO
"""
from abc import ABC, abstractmethod


class IAssociation(ABC):

    @abstractmethod
    def create_association(self) -> any: pass

    @abstractmethod
    def create_new(self) -> any: pass