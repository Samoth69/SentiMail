
import base64
import os
import json
from bucket_call import bucket_call
import pika, os, sys
import mailparser
from check_keywords import check_keywords
from check_links import check_links
from check_spelling import check_spelling
from check_typosquatting import check_typosquatting
from check_character import check_character
import requests
from requests.auth import HTTPBasicAuth
import custom_logger
logger = custom_logger.getLogger("main")

def main():
    logger.info("starting")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queue_send = os.getenv('RABBITMQ_MS_CONTENT', "ms_content")
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
    logger.info("connected")

    channel = connection.channel()

    channel.exchange_declare(exchange="sentimail", exchange_type='direct')

    channel.queue_declare(queue=queue_send)

    channel.queue_bind(exchange="sentimail", queue=queue_send, routing_key="all")

    def callback(ch, method, properties, body):
        logger.info("received %s", json.loads(body))
        # récupérer uniquement la chaine de caractère entre les quotes du body

        file = json.loads(body)
        links, spelling, keywords, typosquatting, character = analyse(file)
        #os.remove(file)
        
        send_result(links, spelling, keywords, typosquatting,character, file)
        #send_result("A", "B", "C", file)

    channel.basic_consume(queue=queue_send, on_message_callback=callback, auto_ack=True)
    logger.info("waiting for messages")
    channel.start_consuming()


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    fi = bucket_call(id_file)
    mail = parseFile(fi)
    """  print(mail)
    print("body", mail.body)
    print("from", mail.from_)
    print("to", mail.to)
    print("subject", mail.subject)
    print("date", mail.date)
    print("server", mail.get_server_ipaddress) """
    #(mailAnalysis, ipAnalysis, spfAnalysis) = analyse_file(id_file)
    links = check_links(mail)
    spelling = check_spelling(mail)
    keywords = check_keywords(mail)
    typosquatting = check_typosquatting(mail)
    character = check_character(mail)
    # remove file
    try:
        os.remove(fi)
    except FileNotFoundError:
        logger.warning("File not found while deleting " + fi)
    except PermissionError:
        logger.warning("permission error while deleting " + fi)
    return links, spelling, keywords, typosquatting, character

def parseFile(id_file):
    mail = mailparser.parse_from_file(id_file)
    return mail


def send_result(links, spelling, keywords, typosquatting,character, uuid):
    # Send result to the API:  
    logger.info("Send result")
    logger.info("Links: %s", links)
    logger.info("Spelling %s", spelling)
    logger.info("Keywords %s", keywords)
    logger.info("Typosquatting: %s", typosquatting)
    logger.info("Character: %s", character)
    user = os.getenv("MS_CONTENT_USER")
    password = os.getenv("MS_CONTENT_PASSWORD")

    # PATCH http://127.0.0.1:8000/api/analysis/uuid/
    data = {
            "responseContentLinks": links,
            "responseContentSpelling": spelling,
            "responseContentKeywords": keywords,
            "responseContentTyposquatting": typosquatting,
            "responseContentCharacter": character,
        }
    url = "http://" + os.getenv("BACKEND_HOST", "127.0.0.1:8000") + "/api/analysis/" + uuid + "/"
    logger.info("URL: %s", url)
    request = requests.patch(url, data = data, auth=HTTPBasicAuth(user, password))
    #request = requests.patch(url, json = data, auth=HTTPBasicAuth(user, password))
    #print("Request: ", request )
    logger.info("Status code: %s", request.status_code)
    if request.status_code > 299:
        logger.error("Invalid return code%s", request.text)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit as e:
            logger.info("System exit")
            raise e
