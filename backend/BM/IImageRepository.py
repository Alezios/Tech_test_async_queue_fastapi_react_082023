from abc import ABC, abstractmethod
from fastapi import UploadFile
from BM.Image import Image


class IImageRepository(ABC):

    @abstractmethod
    def registerImage(self, image: Image):
        pass

    @abstractmethod
    def searchImage(self, keywords: list[str]) -> list[Image]:
        pass

    @abstractmethod
    def getImageById(self, imageId: int) -> Image:
        pass

    @abstractmethod
    def updateImageCaption(self, image: Image):
        pass