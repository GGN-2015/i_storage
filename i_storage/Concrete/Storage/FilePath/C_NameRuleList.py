from ....Abstract.Storage.FilePath.I_NameRuleList import I_NameRuleList
from ....Abstract.Storage.FilePath.I_NameRule import I_NameRule
from ....Abstract.Common.I_Status import I_Status
from ...Common.C_Success import C_Success
from ...Common.C_Failure import C_Failure

# Check Nothing
class _C_NameRule_EmptyRule(I_NameRule):
    def check(self, name:str) -> I_Status:
        return C_Success()

class _C_NameRule_EmptyString(I_NameRule):
    def check(self, name: str) -> I_Status:
        if name == "":
            return C_Failure("file name should not be empty")
        return C_Success()

class _C_NameRule_EndWithDot(I_NameRule):
    def check(self, name:str) -> I_Status:
        if name.endswith("."):
            return C_Failure("file name end with dot")
        return C_Success()

class _C_NameRule_SpaceCharPrefixOrSuffix(I_NameRule):
    def check(self, name:str) -> I_Status:
        if name != name.strip():
            return C_Failure("file name has an empty prefix or suffix")
        return C_Success()

class _C_NameRule_HasSlash(I_NameRule):
    def check(self, name:str) -> I_Status:
        if name.find("/") != -1 or name.find("\\") != -1:
            return C_Failure("file name has slash ('/' or '\\') in it")
        return C_Success()

class _C_NameRule_OtherIllegalChar(I_NameRule):
    def __init__(self,) -> None:
        self._charList = [":", "<", ">", "?", "|", "*", "`", "\"", "\'"]
    def check(self, name:str) -> I_Status:
        for illegalChar in self._charList:
            if name.find(illegalChar) != -1:
                return C_Failure("file name has illegal char '%s' in it" % illegalChar)
        return C_Success()

class _C_NameRule_ControlChar(I_NameRule):
    def __init__(self) -> None:
        self._charList = [
            chr(i)
            for i in range(0, 32) # 0 ~ 31
        ]
    def check(self, name:str) -> I_Status:
        for cchar in self._charList:
            if name.find(cchar) != -1:
                return C_Failure("file name has control char '\\%o' in it" % ord(cchar))
        return C_Success()

class _C_NameRule_WindowsBanName(I_NameRule):
    def __init__(self) -> None:
        self._nameList = [
            "CON", "PRN", "AUX", "NUL"
        ] + [
            ("COM" + str(i)) for i in range(1, 10)
        ] + [
            ("LPT" + str(i)) for i in range(1, 10)
        ]
    def check(self, name:str) -> I_Status:
        for banName in self._nameList:
            if name.upper() == banName:
                return C_Failure("file name %s is banned by windows" % banName)
        return C_Success()

class C_NameRuleList(I_NameRuleList):
    def __init__(self) -> None:
        self._ruleList = [
            _C_NameRule_EmptyString(), # this must be first one
            _C_NameRule_ControlChar(),
            _C_NameRule_EndWithDot(),
            _C_NameRule_SpaceCharPrefixOrSuffix(),
            _C_NameRule_HasSlash(),
            _C_NameRule_OtherIllegalChar(),
            _C_NameRule_WindowsBanName()
        ]

    def getLength(self) -> int:
        return len(self._ruleList)
        
    def getRule(self, idx:int) -> I_NameRule:
        if idx < 0:
            return _C_NameRule_EmptyRule()
        elif idx < len(self._ruleList):
            return self._ruleList[idx]
        else:
            return _C_NameRule_EmptyRule()
