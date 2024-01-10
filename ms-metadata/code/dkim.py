def evaluer_texte(mail):
    mail_headers = mail.headers

    dkim_pass = ["dkim=pass"]
    dkim_unpass = ["dkim=neutral", "dkim=none", "dkim=permerror", "dkim=temperror", "dkim=fail", "DKIM-Signature", "DKIM-Filter"]

    for settings in dkim_pass:
        for header_name, header_value in mail_headers.items():
            if settings in header_value:
                    return "DKIM Exist and Valid"
            
    for settings in dkim_unpass:
        for header_name, header_value in mail_headers.items():
            if settings in header_value:
                    return "DKIM Exist but Unvalid"
				
    return "DKIM Unexist"



