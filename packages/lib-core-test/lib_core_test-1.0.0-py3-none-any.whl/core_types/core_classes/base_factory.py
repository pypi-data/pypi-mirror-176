"""
Base class for any AR factories
"""
from abc import ABC, abstractmethod


class BaseFactory(ABC):
    
    @abstractmethod
    def generate(self, context: str) -> any:
        pass
