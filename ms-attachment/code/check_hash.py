import os
import hashlib
from dotenv import load_dotenv
import requests
import logging

logger = logging.getLogger("check_hash")

def check_hash(mail):

    load_dotenv()
    VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")

    result = "Clean"

    if not os.path.exists("tmp"):
        os.makedirs("tmp")

    url = "https://www.virustotal.com/api/v3/files/"
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY
    }

    mail.write_attachments("tmp")

    # Check hash of each attachment
    for file in os.listdir("tmp"):
        logger.info("file: %s", file)
        with open("tmp/" + file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            logger.info("file_hash: %s", file_hash)
            url = url + file_hash
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                harmless = response.json()["data"]["attributes"]["total_votes"]["harmless"]
                malicious = response.json()["data"]["attributes"]["total_votes"]["malicious"]
                if harmless < malicious and malicious > 0:
                    logger.info("Vote result: Malicious")
                    result = "Malicious"
                last_analysis_results = response.json()["data"]["attributes"]["last_analysis_results"]
                for key in last_analysis_results:
                    #logger.debug("key: %s - %s", key, last_analysis_results[key])
                    #logger.debug("Last analysis result: %s", last_analysis_results[key]["result"])
                    if last_analysis_results[key]["result"] != None:
                        #logger.info("Last analysis result: Malicious")
                        result = "Malicious"
            else:
                logger.error("Error: %s", response.status_code)
                logger.error("response: %s", response)
        os.remove("tmp/" + file)
    logger.info("result: %s", result)
    return result