from pathlib import Path
import pika


class RabbitMQCaptionGeneratorProducer:

    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def produceCaptionRequest(self, imageLocation: Path):
        self.channel.queue_declare(queue='image_captioning')
        self.channel.basic_publish(exchange='', routing_key='image_captioning', body=str(imageLocation))
        print(f" [x] Sent image to queue'")

