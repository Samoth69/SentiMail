#
import base64
import os
import json
from file import analyse_file
from bucket_call import bucket_call
import pika, os, sys
import mailparser
import requests
import custom_logger
logger = custom_logger.getLogger("main")

def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    fi = bucket_call(id_file)
    mail = mailparser.parse_from_file(fi)
    (mail_analysis, ip_analysis, spf_analysis) = analyse_file(mail,fi)

    return mail_analysis, ip_analysis, spf_analysis

def parseFile(id_file):
    mail = mailparser.parse_from_file(id_file)
    return mail
def send_result(mail_result, ip_result, spf_result, uuid):
    # Send result to the API:  
    logger.info("Send result")
    logger.info("Mail: ", mail_result)
    logger.info("IP: ", ip_result)
    logger.info("SPF: ", spf_result)
    user_metadata = os.getenv("MS_METADATA_USER")
    password_metadata = os.getenv("MS_METADATA_PASSWORD")

    # PATCH http://127.0.0.1:8000/api/analysis/uuid/
    data = {
            "responseMetadataIp": ip_result,
            "responseMetadataDomain": mail_result,
            "responseMetadataSPF": spf_result,
        }
    headers = {
        #"Authorization": "Token " + os.getenv("API_KEY"),
        "Authorization": "Basic " + base64.b64encode(bytes(user_metadata + ":" + password_metadata, "utf-8")).decode("ascii"),
    }
    url = "http://" + os.getenv("BACKEND_HOST", "127.0.0.1:8000") + "/api/analysis/" + uuid + "/"
    logger.info("URL: ", url)
    request = requests.patch(url, data = data, headers = headers)
    logger.info("Status code: ", request.status_code)
    if request.status_code > 299:
        logger.error("Error: ", request.text)
    

def main():
    logger.info("Receive")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queue_send = os.getenv('RABBITMQ_MS_METADATA', "ms_metadata")
    virtual_host = os.getenv('RABBITMQ_VHOST', "/")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=host,
            port=port,
            virtual_host=virtual_host,
            credentials=pika.PlainCredentials(user, password)
            )
        )

    channel = connection.channel()

    channel.exchange_declare(exchange="sentimail", exchange_type='direct')

    channel.queue_declare(queue=queue_send)
    channel.queue_bind(exchange="sentimail", queue=queue_send, routing_key="all")

    def callback(ch, method, properties, body):
        logger.info(" [x] Received %r" % json.loads(body))
        # récupérer uniquement la chaine de caractère entre les quotes du body

        file = json.loads(body)
        mail_result, ip_result, spf_result = analyse(file)
        os.remove(file)
        logger.debug(mail_result)
        logger.debug(ip_result)
        logger.debug(spf_result)
        send_result(mail_result, ip_result, spf_result, file)

    channel.basic_consume(queue=queue_send, on_message_callback=callback, auto_ack=True)
    logger.info(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info('Interrupted')
        try:
            sys.exit(0)
        except SystemExit as e:
            raise e
