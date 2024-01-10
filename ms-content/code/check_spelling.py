from langdetect import detect
import language_tool_python



#Recherche les mots correspondant a l'offset
def search_word(mail_canonic, offset):
    current_position = 0
    #Parsage du mail sous forme canonique
    mail_parse = mail_canonic.split()
    for mot in mail_parse:
        longueur_mot = len(mot)
        #Retourne le mot contenant l'offset
        if current_position <= offset < current_position + longueur_mot:
            return mot
        current_position += longueur_mot + 1  
    return None


#Fonction principale
def check_spelling(mail):

    #Extration du corps du message 
    mail_text_plain = mail.text_plain
    mail_text = ''.join(mail_text_plain).replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t').strip()
    if mail_text_plain == []:
        return "Undefined : no text"
    
    #Definition du seuil de frequence de fautes
    #De maniere generale, la longueur moyenne d'un mot est de 5 a 6 lettres
    #Ce chiffre sera arrondi à 6 pour inclure les caracteres tels que la ponctuation

    #La plupart des examens d'ecriture requierent moins d'1 faute tout les 40 mots pour obtenir les meilleures notes
    #On considere qu'un texte comporte environ 1 faute tout les 30 mots
    #A partir de plus d'1 faute tout les 10 mots, on pourra considerer le mail comme mailicieux
    #Soit une frequence de 1 faute tout les 240/60 caracteres

    frequence_clean = 0.0041
    frequence_malicious = 0.017

    #Detection de la langue
    language = detect(mail_text)
    #Parametrage de la verification (langage)
    tool = language_tool_python.LanguageTool(language)
    #Parsage du mail en mots -peut s'averer utile pour l'analyse
    mail_canonic = ' '.join(mail_text.split())

    #Verification
    faults = tool.check(mail_text)

    #Nombre d'erreurs
    fault_number = len(faults)

    

    #Erreur de noms propres non reconnus


    spelling_exception = 0

    for i in range (len(faults)):
        if "SPELLING_RULE" in (faults[i].ruleId):
            spelling_exception = 1
    
            
    if spelling_exception == 1:
        #Parsage du texte avec un unique " " comme separateur entre les mots
        mail_canonic = ' '.join(mail_text.split())
        faults_canonic = tool.check(mail_canonic)

        
        #Si l'erreur est liee a une spelling_rule
        #Rechercher le mot
        #Si le mot commence par une majuscule
        #Retirer la faute : il s'agit tres probablement d'un nom propre nom reconnu

        for i in range (len(faults_canonic)):
            if "SPELLING_RULE" in (faults_canonic[i].ruleId):
                offset = (faults_canonic[i].offset)
                fault_word = search_word(mail_canonic, offset)
                if fault_word != None:
                    if fault_word[0].isupper():
                        fault_number = fault_number - 1



    #Supression des espaces dans le texte
    mail_len = mail_text.replace(" ", "")
    #Calcul frequence de fautes
    frequence_fault = (fault_number)/(len(mail_len))

    #Analyse frequence fautes
    if frequence_fault < frequence_clean:
        return "Clean : good syntax"
    elif frequence_fault < frequence_malicious:
        return "Ok : correct syntax"
    elif frequence_fault >= frequence_malicious:
        return "Malicious : bad syntax"
    