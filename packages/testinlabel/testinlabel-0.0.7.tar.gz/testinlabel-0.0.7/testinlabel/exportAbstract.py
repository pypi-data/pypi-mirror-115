from abc import abstractmethod, ABCMeta
from testindata.dataset.file import File

class ExportAbstract(metaclass=ABCMeta):

    @abstractmethod
    def Exec(self) -> File:pass

