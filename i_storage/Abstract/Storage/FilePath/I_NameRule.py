from abc import ABC, abstractmethod
from ...Common.I_Status import I_Status

class I_NameRule(ABC):
    @abstractmethod
    def check(self, name:str) -> I_Status:
        ...
