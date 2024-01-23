import logging, os, sys
from importlib import reload

def getLogger(name: str):
    # patch de gros crado à cause de cette conneris : https://github.com/jxmorris12/language_tool_python/blob/1ac77366069cce96ba8bd97488efa54f6f93947d/language_tool_python/download_lt.py#L22
    logging.shutdown()
    reload(logging)
    
    log = logging.getLogger(name)
    log.setLevel(level=logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s: %(message)s", 
                                  datefmt="%Y-%m-%d - %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level=logging.DEBUG if "DEBUG" in os.environ else logging.INFO)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log