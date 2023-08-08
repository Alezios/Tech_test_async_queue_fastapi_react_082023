import base64
import io
import json
from pathlib import Path
import pika
import requests


class RabbitMQCaptionGeneratorConsumer:

    CODAIT_MAX_CAPTION_GENERATOR_URL = "http://localhost:5000/model/predict"

    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def startConsumer(self, queueName: str):
        self.channel.queue_declare(queue=queueName)
        self.channel.basic_consume('image_captioning', self.__handleImageMessage, auto_ack=True)
        self.channel.start_consuming()

    def stopConsumer(self):
        self.channel.stop_consuming()
        self.connection.close()

    def __handleImageMessage(self, channel, method, header, body) -> str:
        path = str(body)[2:-1]
        files = {
            'image': (path, open(path, 'rb'), 'image/png'), # This adds the content-type **in** the form-data value (not in the headers)
        }
        maxCaptionGeneratorResponse = requests.post(self.CODAIT_MAX_CAPTION_GENERATOR_URL, files=files,)
        print(maxCaptionGeneratorResponse.text)
