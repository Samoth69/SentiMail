#
import os

from file import *
from bucket_call import *


def analyse(id_file):
    # Initiation de la connexion avec le bucket en fonction de l'ID de l'objet et téléchargement du fichier
    bucket_call(id_file)
    (mailAnalysis, ipAnalysis) = analyse_file(id_file)
    return mailAnalysis, ipAnalysis


mailResult, ipResult = analyse("3.eml")  # TODO ID du fichier à analyser
os.remove("3.eml")
print(mailResult)
print(ipResult)
