#
import os
import json
from file import *
from bucket_call import *
import pika, os, sys

def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    (mailAnalysis, ipAnalysis, spfAnalysis) = analyse_file(id_file)
    return mailAnalysis, ipAnalysis, spfAnalysis

def send_result(mailResult, ipResult, spfResult, uuid):
    # Send result to the API:  
    print("Send result")
    print("Mail: ", mailResult)
    print("IP: ", ipResult)
    print("SPF: ", spfResult)

    # PATCH http://127.0.0.1:8000/api/analysis/uuid/
    data = {
            "responseMetadataIp": ipResult,
            "responseMetadataDomain": mailResult,
            "responseMetadataSPF": spfResult,
        }
    url = "http://" + os.getenv("BACKEND_HOST", "127.0.0.1:8000") + "/api/analysis/" + uuid + "/"
    request = requests.patch(url, data = data)
    print("URL: ", url)

def main():
    print("Receive")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queueSend = os.getenv('RABBITMQ_QUEUE', "sentimail")
    virtualHost = os.getenv('RABBITMQ_VHOST', "/")
    #connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, virtual_host=virtualHost, credentials=pika.PlainCredentials(user, password)))
    #queueSend = os.getenv('RABBITMQ_QUEUE')
    #virtualHost = os.getenv('RABBITMQ_VHOST')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtualHost,
            credentials=pika.PlainCredentials(user, password)
            )
        )

    channel = connection.channel()
    channel.queue_declare(queue=queueSend)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        # récupérer uniquement la chaine de caractère entre les quotes du body

        file = json.loads(body)
        mailResult, ipResult, spfResult = analyse(file)
        os.remove(file)
        print(mailResult)
        print(ipResult)
        print(spfResult)
        send_result(mailResult, ipResult, spfResult, file)

    channel.basic_consume(queue=queueSend, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
