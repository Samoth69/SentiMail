from check_spf import *
import re
from check_reputation import *
import mailparser


def analyse_file(mail, id_file):
    sender_ip = extract_ip(id_file)
    mail_server = extract_sender_server(id_file)
    sender_email = extract_sender_mail(mail, id_file)
    print("result sender ip", sender_ip)
    print("result mail server", mail_server)
    print("result sender email", sender_email)
    if sender_ip != None:
        ipAnalysis = reputation(sender_ip)
    else:
        ipAnalysis = "Erreur - Test non effectué"

    if mail_server != None:
        mailAnalysis = mail_verificator(sender_email)
    else:
        mailAnalysis = "Erreur - Test non effectué"

    spf_check = spf2(sender_ip, sender_email, mail_server)

    return mailAnalysis, ipAnalysis, spf_check


def extract_ip(file_path):
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
                    match = re.search(r'\[([^\]]+)\]',
                                      header)  # Trouver le texte entre les caractères '[' et ']' dans le header
                    if match == None:
                        received_headers = msg.get_all('Authentication-Results')

                        for header in received_headers:
                            if 'spf' in header.lower():
                                match = re.search(r'sender IP is ([\d.]+)', header)
                                if match:
                                    sender_ip = match.group(1)
                                    print("Sender IP:", sender_ip)
                                    return sender_ip

                    if match:
                        sender_ip = match.group(1)  #
                        return sender_ip
                    # Si aucune adresse IP n'est trouvée, afficher un message d'erreur
                    else:
                        print("Aucune adresse IP trouvée.")
                        return None


def extract_sender_server(file_path):
    with open(file_path, 'rb') as file:
        # Utiliser BytesParser pour lire le fichier EML
        msg = BytesParser(policy=policy.default).parse(file)
        # Récupérer l'e-mail du sender (si disponible)
        sender_email_raw = msg.get('From')
        sender_email = None
        # ARC-Authentication-Results: i=1; mx.google.com; Récupérer unique la chaine après ; (mx.google.com)
        mail_server = msg.get('ARC-Authentication-Results')
        # Si ARC-Authentication-Results existe et différent de None
        if mail_server != None:

            mail_server = msg.get('ARC-Authentication-Results')
            mail_server = mail_server.split(";")[1]
            print("Function sender_server", mail_server)
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
                return None
        return mail_server


def extract_sender_mail(mail, file_path):
    mail_from = mail.from_
    print("mail_from", mail_from)
    sender_email = mail_from[-1][-1]
    print("function sender email", sender_email)
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
                return sender_email
    return sender_email
