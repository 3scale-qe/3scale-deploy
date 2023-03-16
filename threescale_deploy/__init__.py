import logging

logger = logging.getLogger("deployer")


def log_exception(message: str, level: int, exception: Exception):
    logger.log(level, message)
    logger.debug(exception, exc_info=True)
