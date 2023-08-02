from fastapi import UploadFile
import re
from BM.ICaptionGenerator import ICaptionGenerator
from BM.IImageRepository import IImageRepository
from pathlib import Path


class Image:

    def __init__(self, file: UploadFile):
        self.imageId = None
        if not self.__checkIsImageFile(file):
            raise TypeError("parameter \'file: UploadFile\' is not an image")
        else:
            self.imageData = file

    async def register(self, repository: IImageRepository):
        self.imageId = await repository.registerNewImage(self.imageData)
        return self.imageId

    def generateCaption(self, captionGenerator: ICaptionGenerator, repository: IImageRepository):
        # if no imageId, then it hasnt been register in filesystem or db. Has to be done first
        if self.imageId is None:
            raise Exception("Cannot generate caption, image is not yet registered in db")
        else:
            path = Path(repository.getImageLocationById(self.imageId))
            caption = captionGenerator.generateCaptionFor(path)
            print(caption)

    def __checkIsImageFile(self, file: UploadFile) -> bool:
        result = True
        if re.match(r'image/+', file.content_type) is None:
            result = False
        return result
