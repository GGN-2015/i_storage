from ....Abstract.Storage.FilePath.I_Path import I_Path
from .C_MutablePath import C_MutablePath

class FileNameNotPermitted(ValueError):
    ...

# immutable path is implemented by mutable path
class C_Path(I_Path):
    def __init__(self, nameList:list[str]) -> None:
        self._mutablePath = C_MutablePath()
        for name in nameList:
            status = self._mutablePath.pushBack(name)
            if not status.isSuccess():
                raise FileNameNotPermitted(name)
    
    def getDepth(self) -> int:
        return self._mutablePath.getDepth()

    def getName(self, idx:int) -> str:
        return self._mutablePath.getName(idx)
