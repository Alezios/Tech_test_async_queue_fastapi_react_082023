from pathlib import Path
import pika


class RabbitMQCaptionGeneratorProducer:

    def __init__(self):
        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters(host='localhost', credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

    def produceCaptionRequest(self, imageRepositoryIdentifier, queueName: str):
        self.channel.queue_declare(queue=queueName)
        self.channel.basic_publish(exchange='', routing_key=queueName, body=str(imageRepositoryIdentifier))
        print(f" [x] Sent image to queue'")

