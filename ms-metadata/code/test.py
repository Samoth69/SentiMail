from email import policy
from email.parser import BytesParser

import mailparser
import re
import json
import spf



import re

import re

def extract_ip(mail):
    print("mail headers", mail.received)
    mail = mail.received

    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')

    for dictionary in mail:
        for key, value in dictionary.items():
            if isinstance(value, str):
                match = ip_pattern.search(value)
                if match:
                    return match.group()

    return None  # Retourne None si aucune adresse IP n'est trouvée


def extract_sender_server(mail):
    message = str(mail.headers)
    print("message", message)
    match = re.search(r'from ([^\s]+)', message)
    if match:
        sender_server= match.group(1)

        print("Sender server:", sender_server)
    else:
        print("Sender server not found")

def extract_sender_mail(mail, file_path):
    mail_from = mail.from_
    print("mail_from", mail_from)
    sender_email = mail_from[-1][-1]
    # si sender_email est vide on affiche erreur
    if sender_email == "":
        with open(file_path, 'rb') as file:
            # Utiliser BytesParser pour lire le fichier EML
            msg = BytesParser(policy=policy.default).parse(file)
            # Récupérer l'e-mail du sender (si disponible)
            sender_email_raw = msg.get('From')
            sender_email = None
            if sender_email_raw:
                # Utiliser une expression régulière pour extraire la partie entre les caractères '<' et '>'
                match = re.search(r'<([^>]+)>', sender_email_raw)

                # Dior, Dior, <laredoute@fr.redoute.com> recuperer la chaine entre <> en faisant attention à la virgule
                if match == None:
                    match = re.search(r'([^\s]+@[^\s]+)', sender_email_raw)
                    if match:
                        sender_email = match.group(1)
                        print("Sender email:", sender_email)
                if match:
                    sender_email = match.group(1)

                print("Ligne 47", sender_email)



# Tests
mail = mailparser.parse_from_file("2.eml")
ip = extract_ip(mail)
print(ip)
extract_sender_mail(mail, "2.eml")
extract_sender_server(mail)