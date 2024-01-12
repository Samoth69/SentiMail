import os
import hashlib
from dotenv import load_dotenv
import requests

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
        print("[check_hash] file: ", file)
        with open("tmp/" + file, "rb") as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
            print("[check_hash] file_hash: ", file_hash)
            url = url + file_hash
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                harmless = response.json()["data"]["attributes"]["total_votes"]["harmless"]
                malicious = response.json()["data"]["attributes"]["total_votes"]["malicious"]
                if harmless < malicious and malicious > 0:
                    print("[check_hash] Vote result: Malicious")
                    result = "Malicious"
                last_analysis_results = response.json()["data"]["attributes"]["last_analysis_results"]
                for key in last_analysis_results:
                    #print("[check_hash] key: ", key, " - ", last_analysis_results[key])
                    #print("[check_hash] Last analysis result: ", last_analysis_results[key]["result"])
                    if last_analysis_results[key]["result"] != None:
                        #print("[check_hash] Last analysis result: Malicious")
                        result = "Malicious"
            else:
                print("[check_hash] Error: ", response.status_code)
                print("[check_hash] response: ", response)
        os.remove("tmp/" + file)
    print("[check_hash] result: ", result)
    return result