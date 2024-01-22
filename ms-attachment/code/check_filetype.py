import logging

logger = logging.getLogger("check_filetype")

def check_filetype(mail):
    """Check if there are malicious file types in the mail
    :param mail: mail object
    :return: "Clean", "Malicious" or "Suspicious"
    """
    malicious_extensions = ["exe", "bat", "cmd", "vbs", "js", "jar", "msi", "scr", "pif", "com", "hta", "cpl", "reg", "wsf", "wsh", "ps1", "rtf", "zip", "rar", "7z", "tar", "gz", "tgz", "bz2", "xz", "iso", "img", "dmg", "bin", "cue", "mdf", "mds", "nrg", "img"]
    suspicious_extensions = ["doc", "docx", "xls", "xlsx", "ppt", "pptx", "pdf"]
    
    attachments = mail.attachments
    for attachment in attachments:
        filename = attachment["filename"]
        extension = filename.split(".")[-1]
        logger.info("Filename: %s", filename)
        logger.info("Extension: %s", extension)
        if extension in malicious_extensions:
            return "Malicious"
        elif extension in suspicious_extensions:
            return "Suspicious"
    return "Clean"