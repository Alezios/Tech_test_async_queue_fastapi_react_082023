from fastapi import FastAPI, UploadFile, status
from pydantic import BaseModel
from typing import Annotated
from DAL.SQLiteDatabase import SQLiteDatabase

app = FastAPI()
database = SQLiteDatabase()

@app.post("/image/upload", status_code=status.HTTP_201_CREATED)
async def uploadImage(image: UploadFile):
    await database.registerNewImage(image)
    return {"message": "image received"}
