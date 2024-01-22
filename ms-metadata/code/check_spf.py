import spf
import custom_logger
logger = custom_logger.getLogger("check_spf")

def spf2(ip, domain, mail_server):
    """Check if SPF record is valid
    :param ip: IP address
    :param domain: domain name
    :param mail_server: mail server
    :return: "SPF record is valid", "SPF record is invalid" or "SPF record does not exist"
    """
    try:
        logger.debug(ip)
        logger.debug(domain)
        logger.debug(mail_server)
        spf_check = spf.check2(ip, domain, mail_server)


        result = spf_check[0]
        logger.info("result %s", result)
        if result == "pass" or result == "neutral":
            return "SPF record is valid"
        else:
            return "SPF record is invalid"
    except Exception as e:
        logger.error("Exception: ", e)
        return "SPF record does not exist"

