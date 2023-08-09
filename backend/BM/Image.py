from fastapi import UploadFile
import re
from pathlib import Path


class Image:

    def __init__(self, file: UploadFile):
        self.imageId = None
        self.path = ""
        self.caption = ""
        self.name = file.filename
        self.mimetype = file.content_type
        if not self.__checkIsImageFile(file):
            raise TypeError("parameter \'file: UploadFile\' is not an image (.png/.jpeg/.jpg)")
        else:
            self.imageData = file.file.read()

    def __checkIsImageFile(self, file: UploadFile) -> bool:
        result = True
        if re.match(r'image/(jpeg|png)', file.content_type) is None:
            result = False
        return result
