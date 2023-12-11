# Récupération du fichier EML (mail) et analyse de son contenu
import os

# Open EML FILE and extract the body with open()
# -----------------------------------------------------------------------------
#
from check_reputation import *


 # def analyse_file(filename):
# with open(filename, "r") as file:
# data = file.read()
        #data = data.split("Sender:")[1]
        #data = data.split(":")[0]

    #with open(filename, "r") as file:
        #ip = file.read()
        #ip = ip.split("X-Mailgun-Sending-Ip: ")[1]
        #ip = ip.split("\n")[0]
    #ipAnalysis = reputation(ip)
# mailAnalysis = mail(data)
# os.remove(filename) # TODO A voir si on supprime le fichier ou pas
# return (mailAnalysis, ipAnalysis)

import email
from email import policy
from email.parser import BytesParser

def analyse_file(file_path):
    with open(file_path, 'rb') as file:
        # Utiliser BytesParser pour lire le fichier EML
        msg = BytesParser(policy=policy.default).parse(file)

        # Récupérer l'adresse IP du sender (si disponible)
        received_headers = msg.get_all('Received')
        sender_ip = None
        if received_headers:
            for header in received_headers:
                if 'from' in header.lower():
                    # Extraire l'adresse IP en utilisant une expression régulière (regex)
                    import re
                    match = re.search(r'\[([^\]]+)\]', header) # Trouver le texte entre les caractères '[' et ']' dans le header
                    if match:
                        sender_ip = match.group(1)
                        break

        # Récupérer l'e-mail du sender (si disponible)
        sender_email_raw = msg.get('From')
        sender_email = None
        if sender_email_raw:
            # Utiliser une expression régulière pour extraire la partie entre les caractères '<' et '>'
            match = re.search(r'<([^>]+)>', sender_email_raw)
            if match:
                sender_email = match.group(1)
            print(sender_email)
            print(sender_ip)
            ipAnalysis = reputation(sender_ip)
            mailAnalysis = mail(sender_email)
            return (mailAnalysis, ipAnalysis)






