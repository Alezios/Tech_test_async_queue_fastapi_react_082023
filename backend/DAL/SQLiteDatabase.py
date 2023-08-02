from fastapi import UploadFile
from BM.IImageRepository import IImageRepository
from datetime import datetime
from pathlib import Path
import sqlite3


class SQLiteDatabase(IImageRepository):

    SQLITE_DB_NAME = "db_images.db"
    SQLITE_DB_DIRECTORY_PATH = Path(__file__).parent / "db/"
    IMAGES_DIRECTORY_PATH = Path(__file__).parent / "db/images/"

    def __init__(self):
        if not self.SQLITE_DB_DIRECTORY_PATH.is_dir():
            self.SQLITE_DB_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.SQLITE_DB_DIRECTORY_PATH / self.SQLITE_DB_NAME)
        self.__checkAndCreateDatabaseTables()

    async def registerNewImage(self, image: UploadFile) -> int:
        imageLocation = await self.__saveImageInFilesystem(image)
        imageId = self.__saveImagePathInDB(imageLocation)
        return imageId


    def searchImage(self, keywords: list[str]):
        pass

    def getImageLocationById(self, imageId: int) -> str:
        cursor = self.connection.cursor()
        cursor.execute("SELECT path from Image WHERE imageId = " + str(imageId))
        path = cursor.fetchone()
        if path is not None:
            return path[0]


    def addCaption(self, imageId: int, caption: str):
        pass

    def __checkAndCreateDatabaseTables(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Image'")
        if cursor.fetchone()[0] != 1:
            print("Table Image doesn't exist. Creating...")
            cursor.execute("CREATE TABLE Image (imageId INTEGER PRIMARY KEY AUTOINCREMENT, path VARCHAR(255) NOT NULL, caption VARCHAR(255))")

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Keyword'")
        if cursor.fetchone()[0] != 1:
            print("Table Keyword doesn't exist. Creating...")
            cursor.execute("CREATE TABLE Keyword (keywordId INTEGER PRIMARY KEY AUTOINCREMENT, keyword VARCHAR(50) UNIQUE)")

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ImageKeyword'")
        if cursor.fetchone()[0] != 1:
            print("Table ImageKeyword doesn't exist. Creating...")
            cursor.execute("CREATE TABLE ImageKeyword (imageKeywordId INTEGER PRIMARY KEY AUTOINCREMENT, imageId INTEGER REFERENCES Images(imageID), keywordId INTEGER REFERENCES Keyword(keywordId))")

        cursor.close()

    async def __saveImageInFilesystem(self, image: UploadFile) -> Path:
        if not self.IMAGES_DIRECTORY_PATH.is_dir():
            self.IMAGES_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        imageFilename = image.filename.split(".")
        imageFilePath = (self.IMAGES_DIRECTORY_PATH / (imageFilename[0] + "_" +
                                                       now.strftime("%d%m%Y%H%M%S") + "." + imageFilename[1]))
        with open(imageFilePath, "wb") as img:
            imgAsBytes = await image.read()
            img.write(imgAsBytes)
            img.close()
        return imageFilePath

    def __saveImagePathInDB(self, pathToImage: Path) -> int:
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Image (path) VALUES ('" + str(pathToImage) + "')")
        self.connection.commit()
        cursor.execute("SELECT imageId FROM Image WHERE path = '" + str(pathToImage) +"'")
        imageId = cursor.fetchone()[0]
        cursor.close()
        return imageId