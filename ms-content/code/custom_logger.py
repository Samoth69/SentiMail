import logging, os, sys
from importlib import reload

has_been_loaded = False

def getLogger(name: str):
    # patch de gros crado à cause de cette conneris : https://github.com/jxmorris12/language_tool_python/blob/1ac77366069cce96ba8bd97488efa54f6f93947d/language_tool_python/download_lt.py#L22
    global has_been_loaded
    if not has_been_loaded:
        reset_logging()
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

# https://stackoverflow.com/a/56810619
def reset_logging():
    manager = logging.root.manager
    manager.disabled = logging.NOTSET
    for logger in manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            logger.setLevel(logging.NOTSET)
            logger.propagate = True
            logger.disabled = False
            logger.filters.clear()
            handlers = logger.handlers.copy()
            for handler in handlers:
                # Copied from `logging.shutdown`.
                try:
                    handler.acquire()
                    handler.flush()
                    handler.close()
                except (OSError, ValueError):
                    pass
                finally:
                    handler.release()
                logger.removeHandler(handler)