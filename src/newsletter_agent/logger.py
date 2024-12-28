import logging
import os


def _create_logger() -> logging.Logger:
    log_level = os.environ.get("LOG_LEVEL", "INFO")
    log = logging.getLogger("newsletter_agent")
    log.setLevel(log_level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


logger = _create_logger()
