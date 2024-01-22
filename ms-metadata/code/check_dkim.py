import custom_logger
logger = custom_logger.getLogger("dkim")

def verify_dkim(mail):
    mail_headers = mail.headers
    print(mail_headers)

    dkim_pass = ["dkim=pass"]
    dkim_unpass = ["DKIM-Signature", "DKIM-Filter", "dkim=neutral", "dkim=none", "dkim=permerror", "dkim=temperror", "dkim=fail"]
    dkim = dkim_pass + dkim_unpass
    print(dkim)

    for setting in dkim:
        if setting in mail_headers:
            if setting in dkim_pass:
                return "DKIM Valid"
            else:
                return "DKIM Ok"
    return "DKIM Unexist"


