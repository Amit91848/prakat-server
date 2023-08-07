import pika
import json


class RabbitMQ:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.crawl_queue = self.channel.queue_declare(
            queue='custom_crawl_queue')
        print("** Connected to RabbitMq **")

    def publish_to_queue(self, body):
        data = json.dumps(body)
        # data = json.dumps(body.dict())
        # self.channel.basic_publish(
        # exchange='', routing_key='custom_crawl_queue', body=data, properties=pika.BasicProperties(content_type='application/json'))
        self.channel.basic_publish(
            exchange='', routing_key='custom_crawl_queue', body=data, properties=pika.BasicProperties(content_type='application/json')
        )
