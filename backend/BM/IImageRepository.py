from abc import ABC, abstractmethod
from fastapi import UploadFile


class IImageRepository(ABC):

    @abstractmethod
    def registerNewImage(self, image: UploadFile) -> int:
        pass

    @abstractmethod
    def searchImage(self, keywords: list[str]):
        pass

    @abstractmethod
    def getImageLocationById(self, imageId: int) -> str:
        pass

    @abstractmethod
    def addCaption(self, imageId: int, caption: str):
        pass