from fastapi import UploadFile
from IRepository import IRepository
from datetime import datetime
from pathlib import Path

class SQLiteDatabase(IRepository):

    SQLITE_DB_LOCATION = "../db/db_images.db"
    IMAGES_DIRECTORY_PATH = Path(__file__).parent / "../db/images/"

    async def registerNewImage(self, image: UploadFile):
        if not self.IMAGES_DIRECTORY_PATH.is_dir():
            self.IMAGES_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        imageFilename = image.filename.split(".")
        absoluteImageFilePath = (self.IMAGES_DIRECTORY_PATH / (imageFilename[0] + "_" +
                                 now.strftime("%d%m%Y%H%M%S") + "." + imageFilename[1])).resolve()
        with open(absoluteImageFilePath, "wb") as img:
            imgAsBytes = await image.read()
            img.write(imgAsBytes)
            img.close()

    def searchImage(self, keywords: list[str]):
        pass
