from ....Abstract.Storage.FilePath.I_MutablePath import I_MutablePath
from .C_NameRuleList import C_NameRuleList
from ....Abstract.Common.I_Status import I_Status

class C_MutablePath(I_MutablePath):
    def __init__(self) -> None:
        self._nameList = []

    def getDepth(self) -> int:
        return len(self._nameList)

    def getName(self, idx:int) -> str:
        if idx < 0:
            return ""
        elif idx < len(self._nameList):
            return self._nameList[idx]
        else:
            return ""

    def pop(self) -> None:
        if len(self._nameList) >= 1:
            self._nameList.pop()

    def pushBack(self, name:str) -> I_Status:
        ruleList = C_NameRuleList()
        status = ruleList.check(name)
        if status.isSuccess():
            self._nameList.append(name)
        return status
