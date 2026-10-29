from ...Abstract.Common.I_Status import I_Status

class C_Success(I_Status):
    def isSuccess(self) -> bool:
        return True
    
    def getFailueReason(self) -> str:
        return ""
    