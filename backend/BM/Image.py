from fastapi import UploadFile
import re
from pathlib import Path


class Image:

    def __init__(self, file: UploadFile = None, imageId: int = None, path: str = "", caption: str = "", name: str = "",
                 mimetype: str = "", imageData: bytes = None):
        self.imageId = imageId
        self.path = path
        self.caption = caption
        # file is not None = new Image received as an UploadFile
        if file is not None:
            self.name = file.filename
            self.mimetype = file.content_type
            if not self.__checkIsImageFile(file):
                raise TypeError("parameter \'file: UploadFile\' is not an image (.png/.jpeg/.jpg)")
            else:
                self.imageData = file.file.read()
        # file is None = Image whose data was retrieved from database
        else:
            self.name = name
            self.mimetype = mimetype
            self.imageData = imageData

    def __checkIsImageFile(self, file: UploadFile) -> bool:
        result = True
        if re.match(r'image/(jpeg|png)', file.content_type) is None:
            result = False
        return result
