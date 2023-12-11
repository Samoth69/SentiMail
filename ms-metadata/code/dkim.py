import dkim


def verify_dkim(message):
    # Verify DKIM signature
    try:
        result = dkim.verify(message)
        if result == None:
            return "DKIM signature is valid"
        else:
            return "DKIM signature is invalid"
    except:
        return "DKIM signature not found"

test = (my-filename)



