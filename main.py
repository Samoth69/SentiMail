#
from file import *
from bucket_call import *


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    (mailAnalysis, ipAnalysis) = analyse_file(id_file)
    return mailAnalysis, ipAnalysis


mailResult, ipResult = analyse("66113902-8e92-11ee-b9d1-0242ac120002")  # TODO ID du fichier à analyser
print(mailResult)
print(ipResult)
