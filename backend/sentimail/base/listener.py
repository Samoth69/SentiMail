from django.conf import settings
import threading
import pika

class ResultListener(threading.Thread):
    """
    Base class for result listeners.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor.
        """
        threading.Thread.__init__(self)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                port=settings.RABBITMQ_PORT,
                virtual_host='/',
                credentials=pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
            ))
        self.channel = connection.channel()
        self.channel.queue_declare(queue='sentimail-responses')
        self.channel.basic_consume(queue='sentimail-responses', on_message_callback=self.callback)
        
    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body}")
        

    def run(self):
        """
        Run the listener.
        """
        self.channel.start_consuming()