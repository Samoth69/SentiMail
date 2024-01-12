import logging, os, sys

def getLogger(name: str):
    log = logging.getLogger(name)
    log.setLevel(level=logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s: %(message)s", 
                                  datefmt="%Y-%m-%d - %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level=logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log