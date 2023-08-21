from abc import ABC, abstractmethod
from BM.Image import Image


class ICaptionGenerator(ABC):

    @abstractmethod
    def generateCaptionFor(self, image: Image):
        pass

