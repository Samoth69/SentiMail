import os
import hashlib
from dotenv import load_dotenv
import requests
import custom_logger

logger = custom_logger.getLogger("check_hash")

def check_hash(mail):
    """Check if there are malicious attachments in the mail using VirusTotal API
    :param mail: mail object
    :return: "Clean" or "Malicious"
    """

    load_dotenv()
    VIRUS_TOTAL_API_KEY = os.getenv("VIRUS_TOTAL_API_KEY")

    result = "Clean"

    
    headers = {
        "accept": "application/json",
        "x-apikey": VIRUS_TOTAL_API_KEY
    }

    mail.write_attachments("/tmp/files")

    # Check hash of each attachment
    for file in os.listdir("/tmp/files"):
        logger.info("file: %s", file)
        url = "https://www.virustotal.com/api/v3/files/"
        with open("/tmp/files/" + file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            logger.info("file: %s", file)
            logger.info("file_hash: %s", file_hash)
            url = url + file_hash
            logger.info("url: %s", url)
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
                logger.error("response: %s", response.text)
        os.remove("/tmp/files/" + file)
    logger.info("result: %s", result)
    return result