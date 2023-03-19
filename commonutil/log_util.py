import os

from enum import Enum, unique

import sys

import json

from typing import Dict

from logging.__init__ import Logger, Formatter

import logging

import logging.handlers

from logging import FileHandler, StreamHandler

from fileutil.file_util import PropertyFileUtil


@unique
class Color(Enum):
    RESET = '\033[0m'
    GREEN = '\033[96m'
    ORANGE = '\033[33m'
    DARKRED = '\033[35m'
    DARKCYAN = '\033[36m'
    PURPLE = '\033[95m'
    RED = '\033[31m'


class MyLogger:
    DEFAULT_LOG_FORMAT: str = '%(asctime)s-%(levelname)s-%(filename)s-%(threadName)s-%(lineno)d-%(funcName)s-%(' \
                              'message)s '
    DEFAULT_LEVEL: int = logging.DEBUG
    DEFAULT_LOG_DIR_NAME: str = "log"
    DEFAULT_ENCODING: str = "utf-8"
    DEFAULT_USE_STD: bool = True

    @staticmethod
    def build(log_dir_path: str,
              use_std_handler: bool = True,
              log_format: str = None,
              log_level: int = None,
              encoding: str = None) -> Logger:
        """
        创建Logger对象
        :param log_dir_path: log文件存放地址
        :param use_std_handler: 是否使用标准输出handler
        :param log_format: log文件记录格式
        :param log_level: all_log文件输出等级
        :param encoding: 日志编码方式
        :return: Logger对象
        """
        logger = logging.getLogger("log")
        error_log_path = log_dir_path + os.sep + "error.log"
        all_log_path = log_dir_path + os.sep + "all.log"

        all_log_handler = MyLogger.build_file_handler(all_log_path, encoding=encoding, log_format=log_format,
                                                      log_level=log_level)
        error_log_handler = MyLogger.build_file_handler(error_log_path, encoding=encoding, log_format=log_format,
                                                        log_level=logging.ERROR)

        logger.addHandler(all_log_handler)
        logger.addHandler(error_log_handler)
        if use_std_handler:
            debug_handler = MyLogger.build_std_handler()
            logger.addHandler(debug_handler)

        return logger

    @staticmethod
    def build_file_handler(log_path: str,
                           encoding: str = None,
                           log_format: str = None,
                           log_level: int = None) -> FileHandler:
        """
        创建文件输出Handler
        :param log_path: 日志文件路径
        :param encoding: 编码方式
        :param log_format: 日志格式
        :param log_level: 默认日志等级
        :return: FileHandler对象
        """
        encoding = encoding if encoding is not None else MyLogger.DEFAULT_ENCODING
        log_format = log_format if log_format is not None else MyLogger.DEFAULT_LOG_FORMAT
        log_level = log_level if log_level is not None else MyLogger.DEFAULT_LEVEL

        handler = logging.FileHandler(log_path, encoding=encoding)
        handler.setFormatter(logging.Formatter(log_format))
        handler.setLevel(log_level)

        return handler

    @staticmethod
    def build_std_handler() -> StreamHandler:
        """
        创建标准输出流Handler
        :return: StreamHandler对象
        """
        level = logging.DEBUG
        handler = logging.StreamHandler(sys.stdout)
        formatter = MyLogger.get_std_colorful_formatter()
        handler.setFormatter(formatter)

        handler.setLevel(level)

        return handler

    @staticmethod
    def get_std_colorful_formatter() -> Formatter:
        """
        获取std彩色输出
        :param level: 日志等级
        :return: Formatter对象
        """
        return logging.Formatter(
            f'{Color.GREEN.value}%(asctime)s{Color.RESET.value}'
            f'-%(levelname)s'
            f'-%(filename)s-%(threadName)s'
            f'-%(lineno)d-%(funcName)s'
            f'-{Color.RED.value}%(message)s{Color.RESET.value}')

    @classmethod
    def __create_log_dir(cls) -> str:
        """
        创建日志文件夹并返回路径
        :return: 日志文件夹
        """
        project_path = os.getcwd()
        all_project_dir_path = []

        for root, dirs, files in os.walk(project_path):
            all_project_dir_path += dirs

        log_dir_path = project_path + os.sep + cls.DEFAULT_LOG_DIR_NAME
        if not os.path.exists(log_dir_path):
            os.mkdir(log_dir_path)

        return log_dir_path

    @classmethod
    def get_logger_from_dict(cls, params_dict: Dict) -> Logger:
        """
        从属性字典中获取Logger对象
        :param params_dict: 属性字典
        :return: Logger对象
        """
        use_std = params_dict.get("use_std", cls.DEFAULT_USE_STD)
        encoding = params_dict.get("encoding", cls.DEFAULT_ENCODING)
        log_format = params_dict.get("log_format", cls.DEFAULT_LOG_FORMAT)
        log_level = params_dict.get("log_level", cls.DEFAULT_LEVEL)
        log_dir_path = MyLogger.__create_log_dir()

        logger = MyLogger.build(log_dir_path, use_std, log_format, log_level, encoding)
        return logger

    @classmethod
    def get_logger_from_json(cls, params: str) -> Logger:
        """
        从json中获得Logger对象
        :param params: Json字符串
        :return: Logger对象
        """
        paras_dict = json.load(params)
        return MyLogger.get_logger_from_dict(paras_dict)

    @classmethod
    def get_logger_from_properties(cls, file_path: str) -> Logger:
        """
        从ini配置文件中获取Logger对象
        :param file_path: ini配置文件路径
        :return: Logger对象
        """
        if not os.path.exists(file_path):
            raise OSError(f"配置文件{file_path}不存在")

        paras_dict = PropertyFileUtil.get_ini_data(file_path, "PROPERTY")
        return MyLogger.get_logger_from_dict(paras_dict)
