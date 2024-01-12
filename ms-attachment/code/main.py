
import base64
import os
import json
#from file import *
from bucket_call import *
import pika, os, sys
import mailparser
import requests
from requests.auth import HTTPBasicAuth
from check_filetype import *
from check_hash import *



def main():
    print("Receive")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queueSend = os.getenv('RABBITMQ_MS_ATTACHMENT', "ms_attachment")
    virtualHost = os.getenv('RABBITMQ_VHOST', "/")

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtualHost,
            credentials=pika.PlainCredentials(user, password)
            )
        )

    channel = connection.channel()

    channel.exchange_declare(exchange="sentimail", exchange_type='direct')

    channel.queue_declare(queue=queueSend)

    channel.queue_bind(exchange="sentimail", queue=queueSend, routing_key="all")

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        # récupérer uniquement la chaine de caractère entre les quotes du body

        file = json.loads(body)
        hash, filetype = analyse(file)
        os.remove(file)
        send_result(hash, filetype, file)
        #send_result("A", "B", "C", file)

    channel.basic_consume(queue=queueSend, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    mail = parseFile(id_file)
    
    #(mailAnalysis, ipAnalysis, spfAnalysis) = analyse_file(id_file)

    hash = check_hash(mail)
    filetype = check_filetype(mail)

    return hash, filetype

def parseFile(id_file):
    mail = mailparser.parse_from_file(id_file)
    return mail


def send_result(hash, filetype, uuid):
    # Send result to the API:  
    print("Send result")
    print("Result hash: ", hash)
    print("Result filetype: ", filetype)
    user = os.getenv("MS_ATTACHMENT_USER")
    password = os.getenv("MS_ATTACHMENT_PASSWORD")

    # PATCH http://127.0.0.1:8000/api/analysis/uuid/
    data = {
            "responseAttachmentHash": hash,
            "responseAttachmentFiletype": filetype,
        }
    url = "http://" + os.getenv("BACKEND_HOST", "127.0.0.1:8000") + "/api/analysis/" + uuid + "/"
    print("URL: ", url)
    request = requests.patch(url, data = data, auth=HTTPBasicAuth(user, password))
    #request = requests.patch(url, json = data, auth=HTTPBasicAuth(user, password))
    #print("Request: ", request )
    print("Status code: ", request.status_code)
    if request.status_code > 299:
        print("Error: ", request.text)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
