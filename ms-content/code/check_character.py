import re
from text_unidecode import unidecode
import logging

logger = logging.getLogger("check_character")


def check_character(mail):
    string = mail.text_plain

    mail = str(string)
    logger.debug("text mail", mail)
    result = est_texte_valide(mail)

    if result == True:
        logger.debug("mail is clean")
        return "Clean"
    else:
        logger.debug("mail is Malicious")
        return "Malicious"
def remove_accents(text): # Fonction pour supprimer les accents
    # Utilisation de la fonction unidecode pour supprimer les accents
    text_without_accents = unidecode(text)

    return text_without_accents


def est_texte_valide(texte): # Fonction pour vérifier si le texte est valide
    # Recupérer uniquement les ou les urls du texte

    # Enlever les urls du texte
    texte = re.sub(r'http\S+', '', texte)
    # Enlever les accents du texte
    texte = remove_accents(texte)
    # Supprimer tous les lettres du texte
    texte = re.sub(r'[a-zA-Z]', '', texte)
    # Supprimer les espaces du texte
    texte = re.sub(r'\s+', '', texte)
    # Supprimer les chiffres du texte
    texte = re.sub(r'[0-9]', '', texte)
    # Récupérer chaque caractère du texte
    mots = [char for char in texte]
    logger.debug(mots)
    # Vérifier chaque mot pour s'assurer qu'il est composé de caractères alphanumériques et est compris avec les caractères de ponctuation ou autre caractères spéciaux normalement utilisés dans les textes

    caractere_valide = ['.', ',', ';', ':', '!', '?',"'",'(',')','/', "\\",'_']

    # Compte chaque caractère du texte et faire un pourcentage de caractère valide.
    caractere_valide_count = 0
    for mot in mots:
        if mot in caractere_valide:
            caractere_valide_count += 1
    logger.debug(caractere_valide_count)
    logger.debug(len(mots))
    pourcentage = caractere_valide_count / len(mots)
    logger.debug(pourcentage)
    if pourcentage > 0.4: # 50% de caractère valide
        return True
    else:
        return False

