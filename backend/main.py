from fastapi import FastAPI, UploadFile, status, HTTPException
from BM.IImageRepository import IImageRepository
from DAL.SQLiteDatabase import SQLiteDatabase
from BM.Image import Image
from BM.RabbitMQCaptionGeneratorService import RabbitMQCaptionGeneratorService
from BM.ImageController import ImageController

app = FastAPI()
database: IImageRepository = SQLiteDatabase()
captionGenerator = RabbitMQCaptionGeneratorService()



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


@app.on_event("shutdown")
def closeConsumer():
    captionGenerator.stopService()

