from commonutil.log_util import MyLogger

logger = MyLogger.get_logger_from_dict({})
logger.info("info")
logger.warning("warn")
logger.debug("debug")
logger.error("error")
