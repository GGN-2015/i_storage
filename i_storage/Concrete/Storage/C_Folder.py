from ...Abstract.Storage.I_Folder import I_Folder
from ...Abstract.Storage.I_DataFile import I_DataFile
from ...Abstract.Storage.FilePath.I_Path import I_Path
from ...Abstract.Common.I_Status import I_Status
from ..Common.W_ErrorWrap import W_ErrorWrap
from ..Common.W_ErrorDefault import W_ErrorDefault
from ..Common.C_Success import C_Success
from ..Common.C_Failure import C_Failure
from .C_DataFile import C_DataFile

from typing import Optional
import os
import shutil

class C_Folder(I_Folder):

    def __init__(self, realAbsPath:str) -> None:
        self._realAbsPath = realAbsPath

    # get the real path in folder on filesystem
    def _getRealPath(self, path:I_Path) -> str:
        filepath = os.path.join(self._realAbsPath, *path.getList())
        return filepath

    # create an empty file if not exists
    def createDataFile(self, path:I_Path) -> I_Status:
        @W_ErrorWrap
        def _f():
            filepath = self._getRealPath(path)
            folderpath = os.path.dirname(filepath)
            os.makedirs(folderpath, exist_ok=True)
            try:
                with open(filepath, "xb"):
                    pass
            except FileExistsError:
                if not os.path.isfile(filepath):
                    raise
            return C_Success()
        return _f()

    # check if is exists as a data file or a folder
    def isExist(self, path:I_Path) -> bool:
        @W_ErrorDefault(False)
        def _f() -> bool:
            filepath = self._getRealPath(path)
            return os.path.exists(filepath)
        return _f()

    # if the aim path is a data file, get it
    def getDataFile(self, path:I_Path) -> Optional[I_DataFile]:
        @W_ErrorDefault(None)
        def _f():
            filepath = self._getRealPath(path)
            if not os.path.isfile(filepath): # is not a file (maybe folder)
                return None
            return C_DataFile(filepath)
        return _f()

    def createFolder(self, path:I_Path) -> I_Status:
        @W_ErrorWrap
        def _f():
            filepath = self._getRealPath(path)
            os.makedirs(filepath, exist_ok=True)
            return C_Success()
        return _f()

    # if the aim path is a folder, get it
    def getFolder(self, path:I_Path) -> Optional["I_Folder"]:
        @W_ErrorDefault(None)
        def _f():
            filepath = self._getRealPath(path)
            if not os.path.isdir(filepath): # not dir (maybe datafile)
                return None
            return C_Folder(filepath)
        return _f()

    # remove a data file or a folder
    def remove(self, path:I_Path) -> I_Status:
        if path.getDepth() == 0:
            return C_Failure("RemoveFolderError('can not remove folder from itslef')")
        @W_ErrorWrap
        def _f():
            filepath = self._getRealPath(path)
            if os.path.isfile(filepath):
                os.remove(filepath)
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath)
            return C_Success()
        return _f()
