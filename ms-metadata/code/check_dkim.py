import custom_logger
logger = custom_logger.getLogger("dkim")



def verify_dkim(mail):

    """Check if DKIM is valid
    :param mail: Mail
    :return: "Malicious", "Ok" or "Clean"
    """
        
    mail_headers = mail.headers

    dkim_pass = ["dkim=pass"]
    dkim_unpass = ["DKIM-Signature", "DKIM-Filter", "dkim=neutral", "dkim=none", "dkim=permerror", "dkim=temperror", "dkim=fail"]
    dkim = dkim_pass + dkim_unpass

    for setting in dkim:
        if setting in mail_headers:
            if setting in dkim_pass:
                return "Clean"
            else:
                return "Ok"
    return "Malicious"


