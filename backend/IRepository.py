from abc import ABC, abstractmethod
from fastapi import UploadFile

class IRepository(ABC):

    @abstractmethod
    def registerNewImage(self, image: UploadFile):
        pass

    @abstractmethod
    def searchImage(self, keywords: list[str]):
        pass