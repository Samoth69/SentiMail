
import base64
import os
import json
#from file import *
from bucket_call import *
import pika, os, sys
import mailparser
from check_keywords import *
from check_links import *
from check_spelling import *
from check_typosquatting import *
from check_character import *
import requests
from requests.auth import HTTPBasicAuth


def main():
    print("Receive")
    host = os.getenv('RABBITMQ_HOST')
    port = os.getenv('RABBITMQ_PORT')
    user = os.getenv('RABBITMQ_USER')
    password = os.getenv('RABBITMQ_PASSWORD')
    queueSend = os.getenv('RABBITMQ_MS_CONTENT', "ms_content")
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
        links, spelling, keywords, typosquatting, character = analyse(file)
        os.remove(file)
        
        send_result(links, spelling, keywords, typosquatting,character, file)
        #send_result("A", "B", "C", file)

    channel.basic_consume(queue=queueSend, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    mail = parseFile(id_file)
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
    return links, spelling, keywords, typosquatting, character

def parseFile(id_file):
    mail = mailparser.parse_from_file(id_file)
    return mail


def send_result(links, spelling, keywords, typosquatting,character, uuid):
    # Send result to the API:  
    print("Send result")
    print("links", links)
    print("spelling", spelling)
    print("keywords", keywords)
    print("typosquatting", typosquatting)
    print("character", character)
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
