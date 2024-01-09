import re
import os
from datetime import datetime, timedelta
import urllib.request

def check_typosquatting(mail):

    update_redflags_domains()

    sender = mail.from_
    content = mail.body
    sender_email = sender[-1][-1]
    sender_domain = sender_email.split("@")[1]
    print("[check_typosquatting] Checking typosquatting for sender domain: ", sender_domain)

    # Extract all url from content
    urls = re.findall(r'(https?://[a-z0-9./:%@?=-]+)', content)

    # Extract all domain from urls
    domains = []
    for url in urls:
        domain = url.split("/")[2]
        domains.append(domain)
    print("[check_typosquatting] Checking typosquatting for domains: ", domains)

    # Check if the sender domain is in the list of redflags domains
    result = "Clean"
    test_domain = domains
    test_domain.append(sender_domain)
    print("[check_typosquatting] Checking typosquatting for test_domain: ", test_domain)
    with open('redflags_domains.txt') as f:
        for line in f:
            if line.startswith("#"):
                continue
            if line.strip() in test_domain:
                print("[check_typosquatting] Found typosquatting domain: ", line.strip())
                result = "Malicious"

    print("[check_typosquatting] Checking typosquatting result: ", result)
    return result

# Update the list of redflags domains from the file redflags_domains.txt
# https://red.flag.domains/
# https://dl.red.flag.domains/red.flag.domains.txt

def update_redflags_domains():
    # Check if the file exists
    if not os.path.isfile('redflags_domains.txt'):
        # Download the file
        try:
            print("[update_redflags_domains] Downloading redflags_domains.txt")
            urllib.request.urlretrieve('https://dl.red.flag.domains/red.flag.domains.txt', 'redflags_domains.txt')
        except:
            print("[update_redflags_domains] Error: Can't download redflags_domains.txt")
            return

    try:
       with open('redflags_domains.txt') as f:
            last_update = f.readline()
            last_update = last_update.split(":")[1]
            last_update = last_update.strip()
            yersterday_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

            if last_update != yersterday_date:
                try:
                    print("[update_redflags_domains] Downloading redflags_domains.txt")
                    urllib.request.urlretrieve('https://dl.red.flag.domains/red.flag.domains.txt', 'redflags_domains.txt')
                except:
                    print("[update_redflags_domains] Error: Can't download redflags_domains.txt")
                    return
    except:
        print("[update_redflags_domains] Error: Can't read redflags_domains.txt")
        return
    