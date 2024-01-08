from langdetect import detect
import language_tool_python

#TODO Execpt NP: Exception regles noms propres

def check_spelling(mail):

    mail_text = mail.body

    #Definition du seuil de frequence de fautes
    #De maniere generale, la longueur moyenne d'un mot est de 5 a 6 lettres
    #Ce chiffre sera arrondi à 6 pour inclure les caracteres tels que la ponctuation

    #La plupart des examens d'ecriture requierent moins d'1 faute tout les 40 mots pour obtenir les meilleures notes
    #On considere qu'un texte comporte environ 1 faute tout les 30 mots
    #A partir de plus d'1 faute tout les 20 mots, on pourra considerer le mail comme mailicieux
    #Soit une frequence de 1 faute tout les 240/120 caracteres

    clean_rate = 0.0041
    malicious_rate = 0.0082


    #Detection de la langue
    language = detect(mail_text)
    #Parametrage de la verification (langage)
    tool = language_tool_python.LanguageTool(language)


    #Verification
    faults = tool.check(mail_text)
    #Supression des espaces dans le texte
    mail_len = mail_text.replace(" ", "")
    #Calcul frequence de fautes
    fault_rate = (len(faults))/(len(mail_len))


    #Analyse frequence fautes
    if fault_rate < clean_rate:
        return "Clean : good syntax"
    elif fault_rate < malicious_rate:
        return "Ok : correct syntax"
    elif fault_rate >= malicious_rate:
        return "Malicious : bad syntax"
