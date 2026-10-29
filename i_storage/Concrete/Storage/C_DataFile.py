from ...Abstract.Storage.I_DataFile import I_DataFile
from ...Abstract.Common.I_Status import I_Status
from ..Common.W_ErrorWrap import W_ErrorWrap
from ..Common.W_ErrorDefault import W_ErrorDefault
from ..Common.C_Success import C_Success

import os

class C_DataFile(I_DataFile):

    # the real path should be given
    def __init__(self, realAbsPath:str) -> None:
        self._realAbsPath = realAbsPath
    
    def getLength(self) -> int:
        return os.path.getsize(self._realAbsPath)

    def getContent(self) -> bytes:
        @W_ErrorDefault(b"")
        def _f():
            with open(self._realAbsPath, "rb") as fp:
                content = fp.read()
            return content
        return _f()

    def setContent(self, newContent:bytes) -> I_Status:
        @W_ErrorWrap
        def _f() -> I_Status:
            with open(self._realAbsPath, "wb") as fp:
                fp.write(newContent)
            return C_Success()
        return _f()

    def append(self, newContent:bytes) -> I_Status:
        @W_ErrorWrap
        def _f() -> I_Status:
            with open(self._realAbsPath, "ab") as fp:
                fp.write(newContent)
            return C_Success()
        return _f()
