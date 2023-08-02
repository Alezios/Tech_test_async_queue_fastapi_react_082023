from fastapi import FastAPI, UploadFile, status, HTTPException
from BM.IImageRepository import IImageRepository
from DAL.SQLiteDatabase import SQLiteDatabase
from BM.Image import Image
from BM.RabbitMQCaptionGeneratorService import RabbitMQCaptionGeneratorService

app = FastAPI()
database: IImageRepository = SQLiteDatabase()
captionGenerator = RabbitMQCaptionGeneratorService()



@app.post("/image/upload", status_code=status.HTTP_201_CREATED)
async def uploadImage(image: UploadFile):
    try:
        modelImage = Image(image)
    except TypeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await modelImage.register(database)
    modelImage.generateCaption(captionGenerator, database)
    return {"message": "image received"}


@app.on_event("shutdown")
def closeConsumer():
    captionGenerator.stopService()

