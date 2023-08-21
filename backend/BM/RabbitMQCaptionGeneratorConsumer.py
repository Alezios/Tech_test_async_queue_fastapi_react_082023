import pika
import requests
from BM.IImageRepository import IImageRepository


class RabbitMQCaptionGeneratorConsumer:

    CODAIT_MAX_CAPTION_GENERATOR_URL = "http://localhost:5000/model/predict"

    def __init__(self, imageRepository: IImageRepository):
        self.imageRepository = imageRepository
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def startConsumer(self, queueName: str):
        self.channel.queue_declare(queue=queueName)
        self.channel.basic_consume(queueName, self.__handleImageMessage, auto_ack=True)
        self.channel.start_consuming()

    def stopConsumer(self):
        self.channel.stop_consuming()
        self.connection.close()

    def __handleImageMessage(self, channel, method, header, body) -> str:
        # with the current configuration of the caption generator service, body should be an image's database id
        imageId = int(body)
        imageToGenerateCaptionFor = self.imageRepository.getImageById(imageId)
        path = imageToGenerateCaptionFor.path
        files = {
            'image': (path, open(path, 'rb'), imageToGenerateCaptionFor.mimetype), # This adds the content-type **in** the form-data value (not in the headers)
        }
        maxCaptionGeneratorResponse = requests.post(self.CODAIT_MAX_CAPTION_GENERATOR_URL, files=files,)
        imageToGenerateCaptionFor.caption = maxCaptionGeneratorResponse.json()["predictions"][0]["caption"]