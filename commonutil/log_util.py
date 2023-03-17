import os
import sys
import json
from typing import Dict
from logging.__init__ import Logger
import logging
import logging.handlers
from logging import Handler


class MyLogger:
    DEFAULT_LOG_FORMAT: AnyStr = '%(asctime)s-%(levelname)s-%(filename)s-%(threadName)s-%(lineno)d-%(funcName)s-%(' \
                                 'message)s '
    DEFAULT_LEVEL: int = logging.DEBUG
    DEFAULT_LOG_NAME: str = "UtilLogger"
    DEFAULT_ENCODING: str = "utf-8"

    def __init__(self) -> None:
        pass

    @classmethod
    def get_logger_from_dict(cls, params_dict: Dict):
        pass

