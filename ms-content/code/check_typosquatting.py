import re
import os
from datetime import datetime, timedelta
import urllib.request
import custom_logger

logger = custom_logger.getLogger("check_typosquatting")

def check_typosquatting(mail):
    """Check if there are typosquatting domains in the mail
    :param mail: mail object
    :return: "Clean" or "Malicious"
    """

    update_redflags_domains()

    sender = mail.from_
    content = mail.body
    sender_email = sender[-1][-1]
    sender_domain = sender_email.split("@")[1]
    logger.info("[check_typosquatting] Checking typosquatting for sender domain: %s", sender_domain)

    # Extract all url from content
    urls = re.findall(r'(https?://[a-z0-9./:%@?=-]+)', content)

    # Extract all domain from urls
    domains = []
    for url in urls:
        domain = url.split("/")[2]
        domains.append(domain)
    logger.info("[check_typosquatting] Checking typosquatting for domains: %s", domains)

    # Check if the sender domain is in the list of redflags domains
    result = "Clean"
    test_domain = domains
    test_domain.append(sender_domain)
    logger.info("[check_typosquatting] Checking typosquatting for test_domain: %s", test_domain)
    with open('/tmp/redflags_domains.txt') as f:
        for line in f:
            if line.startswith("#"):
                continue
            if line.strip() in test_domain:
                logger.info("[check_typosquatting] Found typosquatting domain: %s", line.strip())
                result = "Malicious"

    logger.info("[check_typosquatting] Checking typosquatting result: %s", result)
    return result

# Update the list of redflags domains from the file redflags_domains.txt
# https://red.flag.domains/
# https://dl.red.flag.domains/red.flag.domains.txt

def update_redflags_domains():
    # Check if the file exists
    redflags_domains_file = '/tmp/redflags_domains.txt'
    if not os.path.isfile(redflags_domains_file):
        # Download the file
        try:
            logger.info("[update_redflags_domains] Downloading redflags_domains.txt")
            urllib.request.urlretrieve('https://dl.red.flag.domains/red.flag.domains.txt', redflags_domains_file)
        except Exception as e:
            logger.error("[update_redflags_domains] Error: Can't download redflags_domains.txt - %s", e)
            return
    try:
       with open(redflags_domains_file) as f:
            last_update = f.readline()
            last_update = last_update.split(":")[1]
            last_update = last_update.strip()
            yersterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

            if last_update != yersterday_date:
                try:
                    logger.info("[update_redflags_domains] Downloading redflags_domains.txt")
                    urllib.request.urlretrieve('https://dl.red.flag.domains/red.flag.domains.txt', redflags_domains_file)
                except Exception as e:
                    logger.error("[update_redflags_domains] Error: Can't download redflags_domains.txt - %s", e)
                    return
    except Exception as e:
        logger.error("[update_redflags_domains] Error: Can't read redflags_domains.txt - %s", e)
        return True
    