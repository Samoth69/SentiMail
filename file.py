# Récupération du fichier EML (mail) et analyse de son contenu

# Open EML FILE and extract the body with open()
# -----------------------------------------------------------------------------
#
from check_reputation import *


def analyse_file(filename):
    with open(filename, "r") as file:
        data = file.read()
        data = data.split("Sender:")[1]
        data = data.split(":")[0]

    with open(filename, "r") as file:
        ip = file.read()
        ip = ip.split("X-Mailgun-Sending-Ip: ")[1]
        ip = ip.split("\n")[0]
    ipAnalysis = reputation(ip)
    mailAnalysis = mail(data)
    os.remove(filename) # TODO A voir si on supprime le fichier ou pas
    return (mailAnalysis, ipAnalysis)
