import email
from email import policy
from email.parser import BytesParser
import spf
from check_reputation import *

def spf2(ip, domain, mail_server):
    try:
        print(ip)
        print(domain)
        print(mail_server)
        spf_check = spf.check2(ip, domain, mail_server)


        result = spf_check[0]
        print("result", result)
        if result == "pass" or result == "neutral":
            return "SPF record is valid"
        else:
            return "SPF record is invalid"
    except:
        return "SPF record does not exist"
