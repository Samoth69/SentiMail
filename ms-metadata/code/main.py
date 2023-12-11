#
import os
import json
from file import *
from bucket_call import *
import pika, os, sys

def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    (mailAnalysis, ipAnalysis) = analyse_file(id_file)
    return mailAnalysis, ipAnalysis





def main():
    print("Receive")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port='5672', virtual_host='/',
                                                                   credentials=pika.PlainCredentials('rabbitmq',
                                                                                                     '89yNnzWAH!aBUgYwb2S7xbZ%')))
    channel = connection.channel()
    channel.queue_declare(queue='sentimail')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        # récupérer uniquement la chaine de caractère entre les quotes du body

        file = json.loads(body)
        mailResult, ipResult = analyse(file)
        os.remove(file)
        print(mailResult)
        print(ipResult)

    channel.basic_consume(queue='sentimail', on_message_callback=callback, auto_ack=True)
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
