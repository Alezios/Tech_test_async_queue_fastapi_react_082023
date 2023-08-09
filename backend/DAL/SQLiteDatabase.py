from BM.IImageRepository import IImageRepository
from datetime import datetime
from pathlib import Path
import sqlite3
from BM.Image import Image


class SQLiteDatabase(IImageRepository):

    SQLITE_DB_NAME = "db_images.db"
    SQLITE_DB_DIRECTORY_PATH = Path(__file__).parent / "db/"
    IMAGES_DIRECTORY_PATH = Path(__file__).parent / "db/images/"

    def __init__(self):
        if not self.SQLITE_DB_DIRECTORY_PATH.is_dir():
            self.SQLITE_DB_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.SQLITE_DB_DIRECTORY_PATH / self.SQLITE_DB_NAME)
        self.__checkAndCreateDatabaseTables()

    def registerImage(self, image: Image):
        self.__saveImageInFilesystem(image)
        self.__saveImageInDB(image)


    def searchImage(self, keywords: list[str]) -> Image:
        pass

    def getImageById(self, imageId: int) -> Image:
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT path from Image WHERE imageId = " + str(imageId))
        path = cursor.fetchone()
        if path is not None:
            return path[0]
        """
        pass

    def addCaption(self, imageId: int, caption: str):
        pass

    def __checkAndCreateDatabaseTables(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Image'")
        if cursor.fetchone()[0] != 1:
            print("Table Image doesn't exist. Creating...")
            cursor.execute("CREATE TABLE Image (imageId INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255) NOT NULL, mimetype VARCHAR(50) NOT NULL, path VARCHAR(255) NOT NULL, caption VARCHAR(255))")

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Keyword'")
        if cursor.fetchone()[0] != 1:
            print("Table Keyword doesn't exist. Creating...")
            cursor.execute("CREATE TABLE Keyword (keywordId INTEGER PRIMARY KEY AUTOINCREMENT, keyword VARCHAR(50) UNIQUE)")

        cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='ImageKeyword'")
        if cursor.fetchone()[0] != 1:
            print("Table ImageKeyword doesn't exist. Creating...")
            cursor.execute("CREATE TABLE ImageKeyword (imageKeywordId INTEGER PRIMARY KEY AUTOINCREMENT, imageId INTEGER REFERENCES Images(imageID), keywordId INTEGER REFERENCES Keyword(keywordId))")

        cursor.close()

    def __saveImageInFilesystem(self, image: Image):
        if not self.IMAGES_DIRECTORY_PATH.is_dir():
            self.IMAGES_DIRECTORY_PATH.mkdir(parents=True, exist_ok=True)
        now = datetime.now()
        imageFilename = image.name.split(".")
        imageFilePath = (self.IMAGES_DIRECTORY_PATH / (imageFilename[0] + "_" +
                                                       now.strftime("%d%m%Y%H%M%S") + "." + imageFilename[1]))
        with open(imageFilePath, "wb") as img:
            img.write(image.imageData)
            img.close()
        image.path = imageFilePath

    def __saveImageInDB(self, image: Image):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Image (name, mimetype, path, caption) VALUES ('" + str(image.name) + "', '" +
                       str(image.mimetype) + "', '" + str(image.path) + "', '" + str(image.caption) +"')")
        self.connection.commit()