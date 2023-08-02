import threading
from pathlib import Path
from BM.ICaptionGenerator import ICaptionGenerator
from BM.RabbitMQCaptionGeneratorConsumer import RabbitMQCaptionGeneratorConsumer
from BM.RabbitMQCaptionGeneratorProducer import RabbitMQCaptionGeneratorProducer


class RabbitMQCaptionGeneratorService(ICaptionGenerator):

    QUEUE_NAME = "images_queue"

    def __init__(self):
        self.producer = RabbitMQCaptionGeneratorProducer()
        self.consumer = RabbitMQCaptionGeneratorConsumer()
        self.__startImageConsumer()

    def generateCaptionFor(self, imageLocaton: Path) -> str:
        self.producer.produceCaptionRequest(imageLocaton)
        return ""

    def stopService(self):
        self.consumer.connection.add_callback_threadsafe(callback=self.consumer.stopConsumer)
        self.consumerThread.join(timeout=5)

    def __startImageConsumer(self):
        self.consumerThread = threading.Thread(target=self.consumer.startConsumer, args=(self.QUEUE_NAME,))
        self.consumerThread.start()
