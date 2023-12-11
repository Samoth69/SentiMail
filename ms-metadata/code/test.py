import email
from email import policy
from email.parser import BytesParser

def extract_info_from_eml(file_path):
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

    return sender_ip, sender_email

# Utiliser la fonction avec le chemin de votre fichier EML
file_path = "/ms-metadata/2.eml"
ip, email = extract_info_from_eml(file_path)

# Afficher les résultats

print ("IP: " + ip)
print ("Email: " + email)

