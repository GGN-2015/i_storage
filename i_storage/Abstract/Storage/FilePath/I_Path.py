from abc import ABC, abstractmethod

class I_Path(ABC):

    @abstractmethod
    def getDepth(self) -> int:
        ...

    @abstractmethod
    def getName(self, idx:int) -> str:
        ...

    # get the full name list
    def getList(self) -> list[str]:
        return [
            self.getName(i)
            for i in range(self.getDepth())
        ]
