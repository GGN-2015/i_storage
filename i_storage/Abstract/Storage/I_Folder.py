from .I_File import I_File
from .I_DataFile import I_DataFile
from ..Common.I_Status import I_Status

from abc import abstractmethod
from typing import Optional
from .FilePath.I_Path import I_Path

class I_Folder(I_File):

    # create an empty file if not exists
    @abstractmethod
    def createDataFile(self, path:I_Path) -> I_Status:
        ...

    # check if is exists as a data file or a folder
    @abstractmethod
    def isExist(self, path:I_Path) -> bool:
        ...

    # if the aim path is a data file, get it
    @abstractmethod
    def getDataFile(self, path:I_Path) -> Optional[I_DataFile]:
        ...

    @abstractmethod
    def createFolder(self, path:I_Path) -> I_Status:
        ...

    # if the aim path is a folder, get it
    @abstractmethod
    def getFolder(self, path:I_Path) -> Optional["I_Folder"]:
        ...

    # remove a data file or a folder
    @abstractmethod
    def remove(self, path:I_Path) -> I_Status:
        ...
