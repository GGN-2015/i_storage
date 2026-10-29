from abc import ABC, abstractmethod
from .I_NameRule import I_NameRule
from ...Common.I_Status import I_Status

class _C_Success(I_Status):
    def isSuccess(self) -> bool:
        return True
    def getFailueReason(self) -> str:
        return ""
    
class I_NameRuleList(ABC):
    @abstractmethod
    def getLength(self) -> int:
        ...

    @abstractmethod
    def getRule(self, idx:int) -> I_NameRule:
        ...

    def check(self, name:str) -> I_Status:
        for i in range(self.getLength()):
            rule = self.getRule(i)
            ans = rule.check(name)
            if not ans.isSuccess():
                return ans
        return _C_Success()
