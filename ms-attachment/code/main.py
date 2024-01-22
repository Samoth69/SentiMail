
import base64
import os
import json
from bucket_call import bucket_call
import pika, os, sys
import mailparser
import requests
from requests.auth import HTTPBasicAuth
from check_filetype import check_filetype
from check_hash import check_hash
import custom_logger

logger = custom_logger.getLogger("main")

def main():
    logger.info("Starting")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queue_send = os.getenv('RABBITMQ_MS_ATTACHMENT', "ms_attachment")
    virtual_host = os.getenv('RABBITMQ_VHOST', "/")

    logger.info("connecting to rabbitmq")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=pika.PlainCredentials(user, password)
            )
        )
    logger.info("connected to rabbitmq")

    channel = connection.channel()

    channel.exchange_declare(exchange="sentimail", exchange_type='direct')

    channel.queue_declare(queue=queue_send)

    channel.queue_bind(exchange="sentimail", queue=queue_send, routing_key="all")

    def callback(ch, method, properties, body):
        logger.info(" [x] Received %r" % json.loads(body))
        file = json.loads(body)
        hash, filetype = analyse(file)
        os.remove(file)
        send_result(hash, filetype, file)

    channel.basic_consume(queue=queue_send, on_message_callback=callback, auto_ack=True)
    logger.info(' [*] Waiting for messages.')
    channel.start_consuming()


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    mail = parse_file(id_file)
    attachments = mail.attachments
    #filetype = attachments[0]["mail_content_type"]
    #logger.info("Filetype: %s", filetype)

    if attachments == []:
        msg = "No attachment"
        logger.info(msg)
        return msg, msg 

    hash = check_hash(mail)
    filetype = check_filetype(mail)

    return hash, filetype

def parse_file(id_file):
    mail = mailparser.parse_from_file(id_file)
    return mail

# Send result to the API:  
def send_result(hash, filetype, uuid):
    logger.info("Send result")
    logger.info('Result hash: %s', hash)
    logger.info("Result filetype: %s", filetype)

    user = os.getenv("MS_ATTACHMENT_USER")
    password = os.getenv("MS_ATTACHMENT_PASSWORD")

    data = {
            "responseAttachmentHash": hash,
            "responseAttachmentFiletype": filetype,
        }
    url = "http://" + os.getenv("BACKEND_HOST", "127.0.0.1:8000") + "/api/analysis/" + uuid + "/"
    logger.info("URL: %s", url)
    request = requests.patch(url, data = data, auth=HTTPBasicAuth(user, password))
    
    logger.info("Status code: %s", request.status_code)
    if request.status_code > 299:
        logger.error("Error: %s", request.text)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit as e:
            logger.info("System exit")
            #os._exit(0)
            raise e
