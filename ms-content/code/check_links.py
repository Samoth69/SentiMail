from datetime import timedelta
import datetime
import re
import os
import logging
import urllib.request
import requests
from dotenv import load_dotenv

logger = logging.getLogger("check_links")

def check_links(mail):

    nbMalicious = 0

    body = mail.body

    # Extract all url from content
    urls = re.findall(r'(https?://[a-z0-9./:%@?=-]+)', body)
    #logger.info("[check_links] urls: ", urls)
    if googleSafeBrowsingAPI(urls):
        nbMalicious = 1
    
    for url in urls:
        if isInBlackList(url):
            nbMalicious += 1

    #urltest = "https://www.google.com"
    #isMalicious(urltest)

    """  for url in urls:
        # Check if url is malicious
        nbMalicious = 0
        if isMalicious(url):
            nbMalicious += 1 """
        

    
    logger.info("Result: ", nbMalicious, " malicious links found")

    result = "Clean"
    if nbMalicious > 0:
        result = "Malicious"

    return result

def isMalicious(url):
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

    pass

# Google Safe Browsing API
def googleSafeBrowsingAPI(urls):
    result = "Clean"
    isMalicious = False
    API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')

    threatTypes = [
            "MALWARE",
            "SOCIAL_ENGINEERING",
            "POTENTIALLY_HARMFUL_APPLICATION",
            "UNWANTED_SOFTWARE",
            "CSD_DOWNLOAD_WHITELIST"
        ]

    platformTypes = [
            "WINDOWS",
            "CHROME",
            "LINUX",
            "OSX",
            "IOS",
            "ANDROID"
        ]
    
    threatEntryTypes = [
            "URL",
            "CERT",
            "IP_RANGE"
        ]
    
    threatEntries = []
    for url in urls:
        threatEntries.append({"url": url})
    
    #Test 
    #threatEntries.append({"url": "http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/MALWARE/URL/"})
    #threatEntries.append({"url": "http://testsafebrowsing.appspot.com/apiv4/ANY_PLATFORM/SOCIAL_ENGINEERING/URL/"})

    body = {
        "client": {
            "clientId": "sentimail",
            "clientVersion": "0.1.0"
        },
        "threatInfo": {
            "threatTypes": threatTypes,
            "platformTypes": platformTypes,
            "threatEntryTypes": threatEntryTypes,
            "threatEntries": threatEntries
        }
    }
    url = "https://safebrowsing.googleapis.com/v4/threatMatches:find?key=" + API_KEY
    request = requests.post(url, json = body)
    #logger.info("[googleSafeBrowsingAPI] Status: ", request.status_code)
    if request.status_code > 299:
        logger.error("[googleSafeBrowsingAPI] Error: ", request.text)
    elif request.status_code == 200:
        if request.json() != {}:
            resultthreatType = request.json()["matches"][0]["threatType"]
            logger.debug("[googleSafeBrowsingAPI] Result: ", resultthreatType)
            # Number of malicious links
            result = resultthreatType
            isMalicious = True
        
            
        logger.info("[googleSafeBrowsingAPI] Result: ", result)
    return isMalicious

def isInBlackList(url):
#https://malware-filter.gitlab.io/malware-filter/phishing-filter-agh.txt
    phishingFilter = ["phishing_filter.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_30.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_12.txt
    antiMalwareList = ["anti_malware_list.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_12.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt
    dohVpnProxyBypass = ["doh_vpn_proxy_bypass.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_52.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt
    threatIntelFeeds = ["threat_intel_feeds.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_44.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_18.txt
    phishingArmy = ["phishing_army.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_18.txt"]

    #https://adguardteam.github.io/HostlistsRegistry/assets/filter_42.txt
    malwareList = ["malware_list.txt", "https://adguardteam.github.io/HostlistsRegistry/assets/filter_42.txt"]

    blacklists = [phishingFilter, antiMalwareList, dohVpnProxyBypass, threatIntelFeeds, phishingArmy, malwareList]

    for blacklist in blacklists:
        updateBlackList(blacklist)
    pass

    # convert url to domain name
    # url : http://thebestchois.co.uk/track/o4725
    # domain : thebestchois.co.uk
    domain = url.split("/")[2]


    # Search in blacklists
    for blacklist in blacklists:
        #logger.info("[isInBlackList] Searching in ", blacklist[0])
        file = blacklist[0]
        file = "blacklists/" + file
        try:
            with open(file) as f:
                content = f.read()
                if domain in content:
                    logger.info("[isInBlackList] ", domain, " found in ", file)
                    return True
        except FileNotFoundError:
            logger.error("[isInBlackList] Error: Unable to open ", file)
        except Exception as e:
            logger.error("[isInBlackList] Error: ", e)
    #logger.info("[isInBlackList] ", url, " not found in blacklists")
    return False

def updateBlackList(source):
    folder = "blacklists/"
    if not os.path.exists(folder):
        os.makedirs(folder)

    file = source[0]
    file = folder + file
    url = source[1]
    if not os.path.exists(file):
        try:
            logger.info("[updateBlackList] Downloading ", file)
            urllib.request.urlretrieve(url, file)
        except:
            logger.error("[updateBlackList] Error: Unable to download ", file)
    else:
        try:
            logger.debug("[updateBlackList] Checking ", file)
            with open(file) as f:
                content = f.read()
                
                lastUpdate_match = re.search(r'! Last modified: (.+)', content)
                
                if lastUpdate_match:
                    lastUpdate = lastUpdate_match.group(1)
                    logger.debug("[updateBlackList] Last update: ", lastUpdate)
                else:
                    logger.warning("[updateBlackList] Last update information not found in the file.")
                
                nbExpirationDays_match = re.search(r'\b(\d+)\s+day', content)
                if nbExpirationDays_match:
                    nbExpirationDays = nbExpirationDays_match.group(1).split(" ")[0]
                    
                    logger.debug("[updateBlackList] Expiration: ", nbExpirationDays, " days")

                    lastUpdate = lastUpdate.split("T")[0]
                    lastUpdateDate = datetime.datetime.strptime(lastUpdate, '%Y-%m-%d')
                    logger.debug("[updateBlackList] Last update date: ", lastUpdateDate.strftime('%Y-%m-%d'))
                    expirationDate = datetime.datetime.strptime(lastUpdate, '%Y-%m-%d') + timedelta(days=int(nbExpirationDays))
                    logger.debug("[updateBlackList] Expiration date: ", expirationDate.strftime('%Y-%m-%d'))
                    if datetime.datetime.now() > expirationDate:
                        logger.info("[updateBlackList] File expired")
                        try:
                            logger.info("[updateBlackList] Downloading ", file)
                            urllib.request.urlretrieve(url, file)
                        except:
                            logger.error("[updateBlackList] Error: Unable to download ", file)
        except FileNotFoundError:
            logger.error("[updateBlackList] Error: Unable to open ", file)
        except Exception as e:
            logger.error("[updateBlackList] Error: ", e)



