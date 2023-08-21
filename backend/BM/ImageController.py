from fastapi import UploadFile
from BM.Image import Image
from BM.IImageRepository import IImageRepository
from BM.ICaptionGenerator import ICaptionGenerator


class ImageController:

    def __init__(self, repository: IImageRepository, captionGenerator: ICaptionGenerator):
        self.repository = repository
        self.captionGenerator = captionGenerator

    def createImageFromUploadFile(self, imageFile: UploadFile) -> Image:
        image = Image(imageFile)
        return image


    def registerImage(self, image: Image):
        self.repository.registerImage(image)
        self.__generateCaptionForImage(image)

    def __generateCaptionForImage(self, image: Image):
        """
        if self.imageId is None:
            raise Exception("Cannot generate caption, image is not yet registered in db")
        else:
            path = Path(repository.getImageLocationById(self.imageId))
            caption = captionGenerator.generateCaptionFor(path)
            print(caption)
        """
        self.captionGenerator.generateCaptionFor(image)

