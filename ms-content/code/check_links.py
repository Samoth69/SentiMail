from datetime import timedelta
import datetime
import re
import os
import custom_logger
import urllib.request
import requests
import tempfile
from dotenv import load_dotenv

logger = custom_logger.getLogger("check_links")
last_update_blacklists = ""

def check_links(mail):
    """Check if there are malicious links in the mail
    :param mail: mail object
    :return: "Clean" or "Malicious"
    """
    nb_malicious = 0

    body = mail.body

    # Extract all url from content
    urls = re.findall(r'(https?://[a-z0-9./:%@?=-]+)', body)
    
    #logger.info("[check_links] urls: ", urls)
    if googleSafeBrowsingAPI(urls):
        nb_malicious = 1
    
    for url in urls:
        if isInBlackList(url):
            nb_malicious += 1
    
    logger.info("Result: %d malicious links found", nb_malicious)

    result = "Clean"
    if nb_malicious > 0:
        result = "Malicious"

    return result

def is_malicious(url):
    # TO DO
    # - IP address
    #    - Reputation
    #    - Country
    # - Domain name
    # - URL shortener
    # - Redirect
    # - In black list
    # Google Safe Browsing API

    #ip_address = dns.resolver.query(url, 'A')
    #ip_address = socket.gethostbyname(url)
    #logger.info("[isMalicious] ip_address: ", ip_address)
    isInBlackList(url)


# Google Safe Browsing API
def googleSafeBrowsingAPI(urls):
    """Check if there are malicious links in the mail using Google Safe Browsing API
    :param urls: list of urls
    :return: True or False
    """
    result = "Clean"
    is_malicious = False
    API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')

    threat_types = [
            "MALWARE",
            "SOCIAL_ENGINEERING",
            "POTENTIALLY_HARMFUL_APPLICATION",
            "UNWANTED_SOFTWARE",
            "CSD_DOWNLOAD_WHITELIST"
        ]

    platform_types = [
            "WINDOWS",
            "CHROME",
            "LINUX",
            "OSX",
            "IOS",
            "ANDROID"
        ]
    
    threat_entry_types = [
            "URL",
            "CERT",
            "IP_RANGE"
        ]
    
    threat_entries = []
    for url in urls:
        threat_entries.append({"url": url})
    
    #Test 
    #threat_entries.append({"url": "http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/"})
    #threat_entries.append({"url": "http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/"})

    body = {
        "client": {
            "clientId": "sentimail",
            "clientVersion": "0.1.0"
        },
        "threatInfo": {
            "threatTypes": threat_types,
            "platformTypes": platform_types,
            "threatEntryTypes": threat_entry_types,
            "threatEntries": threat_entries
        }
    }
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY
    request = requests.post(url, json = body)
    #logger.info("[googleSafeBrowsingAPI] Status: ", request.status_code)
    if request.status_code > 299:
        logger.error("[googleSafeBrowsingAPI] Error: %s", request.text)
    elif request.status_code == 200:
        if request.json() != {}:
            result_threat_type = request.json()["matches"][0]["threatType"]
            logger.debug("[googleSafeBrowsingAPI] Result: %s", result_threat_type)
            # Number of malicious links
            result = result_threat_type
            is_malicious = True
        
            
        logger.info("[googleSafeBrowsingAPI] Result: %s", result)
    return is_malicious

def isInBlackList(url):
    """Check if the url is in the blacklists
    :param url: url
    :return: True or False
    """
    #https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt
    phishing_filter = ["phishing_filter.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_30.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_12.txt
    anti_malware_list = ["anti_malware_list.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_12.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt
    doh_vpn_proxy_bypass = ["doh_vpn_proxy_bypass.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt
    threat_intel_feeds = ["threat_intel_feeds.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_18.txt
    phishing_army = ["phishing_army.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_18.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_42.txt
    malware_list = ["malware_list.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_42.txt"]

    blacklists = [phishing_filter, anti_malware_list, doh_vpn_proxy_bypass, threat_intel_feeds, phishing_army, malware_list] 

    # Update blacklists
    global last_update_blacklists
    if last_update_blacklists == "":
        logger.info("[isInBlackList] Downloading blacklists")
        for blacklist in blacklists:
            updateBlackList(blacklist)
        last_update_blacklists = datetime.datetime.now()
    elif datetime.datetime.now() > last_update_blacklists + timedelta(days=1):
        logger.info("[isInBlackList] Updating blacklists")
        for blacklist in blacklists:
            updateBlackList(blacklist)
        last_update_blacklists = datetime.datetime.now()
        


    

    # convert url to domain name
    # url : http://thebestchois.co.uk/track/o4725
    # domain : thebestchois.co.uk
    domain = url.split("/")[2]


    # Search in blacklists
    for blacklist in blacklists:
        #logger.info("[isInBlackList] Searching in ", blacklist[0])
        file = blacklist[0]
        file = "/tmp/blacklists/" + file
        try:
            with open(file) as f:
                content = f.read()
                if domain in content:
                    logger.info("[isInBlackList] %s found in %s", domain, file)
                    return True
        except FileNotFoundError:
            logger.error("[isInBlackList] Error: Unable to open %s", file)
        except Exception as e:
            logger.error("[isInBlackList] Error: %s", e)
    #logger.info("[isInBlackList] ", url, " not found in blacklists")
    return False

def updateBlackList(source):
    """  folder = "blacklists/"
    if not os.path.exists(folder):
        os.makedirs(folder) """
    """     temp_dir = tempfile.mkdtemp()
    folder = os.path.join(temp_dir, 'blacklists/')
    logger.debug("[updateBlackList] folder: %s", folder)

    if not os.path.exists(folder):
        os.makedirs(folder)
        logger.info("[updateBlackList] Folder created: %s", folder) """

    folder = "/tmp/blacklists/"
    if not os.path.exists(folder):
        os.makedirs(folder)
        logger.info("[updateBlackList] Folder created: %s", folder)

    file = source[0]
    file = folder + file
    url = source[1]
    if not os.path.exists(file):
        try:
            logger.info("[updateBlackList] Downloading %s", file)
            # urllib.request.urlretrieve(url, file)
            download_file(url, file)
            logger.info("[updateBlackList] done")
        except Exception as e:
            logger.error("[updateBlackList] Error: Unable to download %s", file, " - ", e)
    else:
        try:
            logger.debug("[updateBlackList] Checking %s", file)
            with open(file) as f:
                content = f.read()
                
                last_update_match = re.search(r'! Last modified: (.+)', content)
                
                if last_update_match:
                    last_update = last_update_match.group(1)
                    logger.debug("[updateBlackList] Last update: %s", last_update)
                else:
                    logger.warning("[updateBlackList] Last update information not found in the file.")
                
                nb_expiration_days_match = re.search(r'\b(\d+)\s+day', content)
                if nb_expiration_days_match:
                    nb_expiration_days = nb_expiration_days_match.group(1).split(" ")[0]
                    
                    logger.debug("[updateBlackList] Expiration: %s", nb_expiration_days)

                    last_update = last_update.split("T")[0]
                    last_update_date = datetime.datetime.strptime(last_update, '%Y-%m-%d')
                    logger.debug("[updateBlackList] Last update date: %s", last_update_date.strftime('%Y-%m-%d'))
                    expiration_date = datetime.datetime.strptime(last_update, '%Y-%m-%d') + timedelta(days=int(nb_expiration_days))
                    logger.debug("[updateBlackList] Expiration date: %s", expiration_date.strftime('%Y-%m-%d'))
                    if datetime.datetime.now() > expiration_date:
                        logger.info("[updateBlackList] File expired")
                        try:
                            logger.info("[updateBlackList] Downloading %s", file)
                            urllib.request.urlretrieve(url, file)
                        except Exception as e:
                            logger.error("[updateBlackList] Error: Unable to download %s", file, " - ", e)
        except FileNotFoundError:
            logger.error("[updateBlackList] Error: Unable to open %s", file)
        except Exception as e:
            logger.error("[updateBlackList] Error: %s", e)

# https://stackoverflow.com/a/16696317
def download_file(url, path = None):
    if path is None:
        local_filename = url.split('/')[-1]
    else:
        local_filename = path
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return local_filename