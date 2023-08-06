"""
Base class to wrap any interation with a database SDK or client
"""
from abc import ABC, abstractmethod


class BaseDatabase(ABC):
    
    @abstractmethod
    def query(self, data: any) -> any: pass

    @abstractmethod
    def create_client(self): pass

    @abstractmethod
    def destroy_client(self): pass