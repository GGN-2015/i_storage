from abc import abstractmethod
from .I_File import I_File
from ..Common.I_Status import I_Status

class I_DataFile(I_File):

    @abstractmethod
    def getLength(self) -> int:
        ...

    @abstractmethod
    def getContent(self) -> bytes:
        ...

    @abstractmethod
    def setContent(self, newContent:bytes) -> I_Status:
        ...

    @abstractmethod
    def append(self, newContent:bytes) -> I_Status:
        ...
