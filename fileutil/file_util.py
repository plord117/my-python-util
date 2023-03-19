import os
from typing import List, AnyStr
from configparser import ConfigParser
import csv
import shutil
from configparser import NoSectionError
from xml.etree import ElementTree as et


class PropertyFileUtil:
    @staticmethod
    def get_ini_data(file_path: str, item_name: str, encoding='utf-8'):
        return PropertyFileUtil.read_items_data(file_path, item_name, encoding)

    @staticmethod
    def read_items_data(
            file_path: str,
            item_name: str,
            encoding: str = 'utf-8'):
        """
        读取ini配置文件指定块信息

        :param file_path: 字符串型，配置文件名称
        :param item_name: 字符串型，指定块名称
        :param encoding: 字符串型，指定编码方式
        :return: 配置文件字典dict[str,str]
        """
        # 获得ini读取对象
        parser = PropertyFileUtil.get_ini_parser(file_path, encoding=encoding)
        # 获取块信息
        sections = parser.sections()

        if item_name not in sections:
            raise NoSectionError(f"{file_path}配置文件中{item_name}块不存在")

        # 读取块信息
        items = parser.items(item_name)

        return {key: value for key, value in items}

    # 初始ini处理器
    @staticmethod
    def get_ini_parser(file_name: str, encoding: str):
        """
        初始化ini文件处理器
        :param file_name: 字符串型，ini文件名称
        :param encoding: 字符串型，指定编码方式
        :return: ini配置文件读取对象
        """

        # 初始化读取对象
        conf = ConfigParser()
        # 读取配置文件
        conf.read(file_name, encoding=encoding)

        # 返回配置文件的读取对象
        return conf
