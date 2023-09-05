import re
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
        self.connection = sqlite3.connect(self.SQLITE_DB_DIRECTORY_PATH / self.SQLITE_DB_NAME, check_same_thread=False)
        self.__checkAndCreateDatabaseTables()

    def registerImage(self, image: Image):
        self.__saveImageInFilesystem(image)
        self.__saveImageInDB(image)


    def searchImage(self, keywords: list[str]) -> list[Image]:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Image WHERE imageId IN (SELECT imageId FROM ImageKeyword ik JOIN Keyword k ON ik.keywordId=k.keywordId WHERE k.keyword IN (%s))" % ",".join("?"*len(keywords)), keywords)
        images = cursor.fetchall()
        imagesAsObj = []
        if len(images) == 0:
            print("SQLiteDatabase has no image corresponding with keywords : %s" % " ".join(keywords))
            cursor.close()
        else:
            for i in images:
                imagesAsObj.append(Image(imageId=i[0], name=i[1], mimetype=i[2], path=i[3], caption=i[4]))
            cursor.close()
        return imagesAsObj

    def getImageById(self, imageId: int) -> Image:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * from Image WHERE imageId = " + str(imageId))
        image = cursor.fetchone()
        imageAsObj = None
        if image is None:
            print("SQLiteDatabase has no image with id : " + str(imageId))
            cursor.close()
        else:
            print(image)
            imageAsObj = Image(imageId=image[0], name=image[1], mimetype=image[2], path=image[3], caption=image[4])
            cursor.close()
        return imageAsObj

    def updateImageCaption(self, image: Image):
        cursor = self.connection.cursor()
        # check if image is already known
        cursor.execute("SELECT imageId from Image WHERE imageId="+str(image.imageId))
        if cursor.fetchone() is None:
            raise IndexError("Image with id: " + str(image.imageId) + ", does not exist in SQLiteDatabase")
        else:
            # for the first iteration of this project, we only update the caption as other parameters
            # aren't supposed to change
            cursor.execute("UPDATE Image SET caption = '" + image.caption + "' WHERE imageId=" + str(image.imageId))
            self.connection.commit()
            # insert keywords from the caption into the Keyword table. Ignore insertion if the same keyword is already
            # present in the table
            keywords = re.compile("\w+").findall(image.caption)
            # adding square brackets to keywords because the following executemany expects nested structures to bind
            # parameters 
            for i in range(len(keywords)):
                keywords[i] = [keywords[i]]
            cursor.executemany("INSERT OR IGNORE INTO Keyword(keyword) VALUES(?)", keywords)
            self.connection.commit()
            cursor.executemany("INSERT INTO ImageKeyword(imageId, keywordId) VALUES (" + str(image.imageId)
                               + ",(SELECT keywordId FROM Keyword WHERE keyword = ?))", keywords)
            self.connection.commit()


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
        # update image autoincremented id (filthy)
        cursor.execute("SELECT MAX(imageId) FROM Image")
        image.imageId = int(cursor.fetchone()[0])