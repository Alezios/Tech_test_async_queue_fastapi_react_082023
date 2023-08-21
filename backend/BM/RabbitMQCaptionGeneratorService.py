import threading
from BM.ICaptionGenerator import ICaptionGenerator
from BM.IImageRepository import IImageRepository
from BM.Image import Image
from BM.RabbitMQCaptionGeneratorConsumer import RabbitMQCaptionGeneratorConsumer
from BM.RabbitMQCaptionGeneratorProducer import RabbitMQCaptionGeneratorProducer


class RabbitMQCaptionGeneratorService(ICaptionGenerator):

    QUEUE_NAME = "image_captioning"

    def __init__(self, imageRepository: IImageRepository):
        self.producer = RabbitMQCaptionGeneratorProducer()
        self.consumer = RabbitMQCaptionGeneratorConsumer(imageRepository)
        self.__startImageConsumer()

    def generateCaptionFor(self, image: Image):
        self.producer.produceCaptionRequest(imageRepositoryIdentifier=image.imageId, queueName=self.QUEUE_NAME)
        return ""

    def stopService(self):
        self.consumer.connection.add_callback_threadsafe(callback=self.consumer.stopConsumer)
        self.consumerThread.join(timeout=5)

    def __startImageConsumer(self):
        self.consumerThread = threading.Thread(target=self.consumer.startConsumer, args=(self.QUEUE_NAME,))
        self.consumerThread.start()
