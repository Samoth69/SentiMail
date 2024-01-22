# Micro Service Metadata: reputation (Check reputation of IP address , mail address, domain name)
# -----------------------------------------------------------------------------

import requests
import os
from dotenv import load_dotenv

load_dotenv()
def reputation(ip):
    """Check if IP is malicious
    :param ip: IP address
    :return: "Malicious", "Clean" or "Unknown"
    """
    url = "https://api.greynoise.io/v3/community/" + ip

    headers = {
        'key': os.getenv('GREYNOISE_KEY')
    }

    response = requests.request("GET", url, headers=headers)

    response_json = response.json()
    result = is_malicious(response_json)
    return result

# Check simple de la classification de l'IP

def is_malicious(response_json):

    if 'classification' in response_json:
        if response_json['classification'] == "malicious":
            return "Malicious"
        else:
            return "Clean"
    else:
        return "Unknown"


def mail_verificator(data):
    """Check if mail address is malicious
    :param data: mail address
    :return: "Malicious", "Clean" or "Unknown"
    """
    url = "https://api.apilayer.com/spamchecker?threshold=threshold"

    payload = data.encode("utf-8")
    headers = {
        "apikey": os.getenv('SPAMCHECKER_API_KEY')
    }



    response = requests.request("POST", url, headers=headers, data=payload)

    # Si code retour 200
    if response.status_code == 200:
        response_json = response.json()

        # Check If domain name is malicious
        # Check if is_spam exists in response_json
        if 'is_spam' in response_json:
            if response_json['is_spam'] == "True":
                return "Malicious"
            else:
                return "Clean"
        else:
            return "Unknown"
    else:
        return "erreur"


