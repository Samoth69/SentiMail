import re

def check_keywords(mail):
    print("[check_keywords] Start")

    # English:
    spam_keywords_en = ["viagra", "offer", "free", "business", "opportunity", "loan", "money", "cash", "urgent", "important", "bank", "transfer", "transaction", "investment", "financial", "guarantee", "credit", "debt", "insurance", "beneficiary", "claim", "winner", "winnings", "prize", "award", "lottery", "inheritance", "fund", "charity", "donation", "proposal", "contract", "invoice", "payment", "settlement", "bill", "fee", "cost", "charge", "tax", "duty", "penalty", "fine"]

    phishing_keywords_en = ["verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username", "verify", "confirm", "update", "account", "suspend", "limit", "login", "password", "username"]
    
    # French:
    spam_keywords_fr = ["viagra", "offre", "gratuit", "business", "opportunité", "prêt", "argent", "urgent", "important", "banque", "transfert", "transaction", "investissement", "financier", "garantie", "crédit", "dette", "assurance", "bénéficiaire", "réclamation", "gagnant", "gains", "prix", "loterie", "héritage", "fonds", "charité", "don", "proposition", "contrat", "facture", "paiement", "règlement", "facture", "frais", "coût", "charge", "taxe", "droit", "pénalité", "amende"]

    phishing_keywords_fr = ["vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur", "vérifier", "confirmer", "mettre à jour", "compte", "suspendre", "limite", "connexion", "mot de passe", "nom d'utilisateur"]

    # Full:
    spam_keywords = spam_keywords_en + spam_keywords_fr
    phishing_keywords = phishing_keywords_en + phishing_keywords_fr

    content = mail.body
    subject = mail.subject
    #print(content)

    content = content.lower()

    spam_score = 0
    phishing_score = 0
    spam_score_content = 0
    phishing_score_content = 0
    spam_score_subject = 0
    phishing_score_subject = 0

    for keyword in spam_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', content):
            spam_score_content += 1
    
    for keyword in phishing_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', content):
            phishing_score_content += 1
    
    for keyword in spam_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', subject):
            spam_score_subject += 1
    
    for keyword in phishing_keywords:
        if re.search(r'\b' + re.escape(keyword) + r'\b', subject):
            phishing_score_subject += 1
    
    # Average of the two scores
    spam_score = (spam_score_content + spam_score_subject) / 2
    phishing_score = (phishing_score_content + phishing_score_subject) / 2

    if spam_score > 0 and spam_score > phishing_score:
        print("[check_keywords] End: Spam (score: " + str(spam_score) + ")")
        return "Spam"
    elif phishing_score > 0 and phishing_score > spam_score:
        print("[check_keywords] End: Phishing (score: " + str(phishing_score) + ")")
        return "Phishing"
    else:
        print("[check_keywords] End: Clean")
        return "Clean"


