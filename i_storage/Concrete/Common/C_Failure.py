from ...Abstract.Common.I_Status import I_Status

class C_Failure(I_Status):
    def __init__(self, msg:str) -> None:
        self._msg = msg

    def isSuccess(self) -> bool:
        return False
    
    def getFailueReason(self) -> str:
        return self._msg
