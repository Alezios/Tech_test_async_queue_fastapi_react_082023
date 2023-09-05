import re

from fastapi import FastAPI, UploadFile, status, HTTPException
from BM.IImageRepository import IImageRepository
from DAL.SQLiteDatabase import SQLiteDatabase
from BM.Image import Image
from BM.RabbitMQCaptionGeneratorService import RabbitMQCaptionGeneratorService
from BM.ImageController import ImageController
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database: IImageRepository = SQLiteDatabase()
captionGenerator = RabbitMQCaptionGeneratorService(database)

@app.post("/image/upload", status_code=status.HTTP_201_CREATED)
async def uploadImage(image: UploadFile):
    imageController = ImageController(database, captionGenerator)
    try:
        imageModel = imageController.createImageFromUploadFile(image)
    except TypeError as error:
        print("TypeError : {0}".format(error))
        raise HTTPException(status_code=400, detail="TypeError : {0}".format(error),)
    imageController.registerImage(imageModel)
    return {"message": "image received"}

@app.get("/image/search")
async def searchImage(query: str):
    # TODO Ajouter le traitement des query pour empêcher les injections SQL/XSS
    keywords = re.compile("\w+").findall(query)
    imagesAsObj = database.searchImage(keywords)
    if len(imagesAsObj) == 0:
        return []
    else:
        imagePath = []
        for i in imagesAsObj:
            imagePath.append(i.path)
        return imagePath

@app.on_event("shutdown")
def closeConsumer():
    captionGenerator.stopService()

