# Récupération du fichier EML (mail) et analyse de son contenu
import os

# Open EML FILE and extract the body with open()
# -----------------------------------------------------------------------------
#
from check_reputation import *
from check_spf import *
import re

# def analyse_file(filename):
# with open(filename, "r") as file:
# data = file.read()
# data = data.split("Sender:")[1]
# data = data.split(":")[0]

# with open(filename, "r") as file:
# ip = file.read()
# ip = ip.split("X-Mailgun-Sending-Ip: ")[1]
# ip = ip.split("\n")[0]
# ipAnalysis = reputation(ip)
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
                    if match == None:
                        received_headers = msg.get_all('Authentication-Results')

                        for header in received_headers:
                            if 'spf' in header.lower():
                                match = re.search(r'sender IP is ([\d.]+)', header)
                                if match:
                                    sender_ip = match.group(1)
                                    print("Sender IP:", sender_ip)
                                    break

                    if match:
                        sender_ip = match.group(1)
                        break
                    # Si match

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

            print("Ligne 47",sender_email)
            print(sender_ip)
            ipAnalysis = reputation(sender_ip)
            mailAnalysis = mail(sender_email)
            # ARC-Authentication-Results: i=1; mx.google.com; Récupérer unique la chaine après ; (mx.google.com)
            mail_server = msg.get('ARC-Authentication-Results')
            # Si ARC-Authentication-Results existe et différent de None
            if mail_server != None:

                mail_server = msg.get('ARC-Authentication-Results')
                mail_server = mail_server.split(";")[1]
                print("Premiere", mail_server)
            else:

                result_string = msg.get('Authentication-Results')
                # Utilisation de l'expression régulière pour extraire la chaîne
                match = re.search(r'smtp.mailfrom=(.*?);', result_string)

                # Vérification de la correspondance
                if match:
                    mail_server = match.group(1)
                    print("Mail 2", mail_server)
                else:
                    print("Aucune correspondance trouvée.")


            spf_check = spf2(sender_ip, sender_email, mail_server)
            return mailAnalysis, ipAnalysis, spf_check
