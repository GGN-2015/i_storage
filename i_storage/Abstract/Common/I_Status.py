from abc import ABC, abstractmethod

class I_Status(ABC):

    @abstractmethod
    def isSuccess(self) -> bool:
        ...

    @abstractmethod
    def getFailueReason(self) -> str:
        ...
