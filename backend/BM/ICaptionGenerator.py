from abc import ABC, abstractmethod
from pathlib import Path

class ICaptionGenerator(ABC):

    @abstractmethod
    def generateCaptionFor(self, imageLocation: Path) -> str:
        pass

