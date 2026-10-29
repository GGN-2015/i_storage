from .I_Path import I_Path
from abc import abstractmethod
from ...Common.I_Status import I_Status

class I_MutablePath(I_Path):
    
    @abstractmethod
    def pop(self) -> None:
        ...

    @abstractmethod
    def pushBack(self, name:str) -> I_Status:
        ...
