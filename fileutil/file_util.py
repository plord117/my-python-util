import os

from typing import Dict, List

from configparser import ConfigParser

import csv

import shutil

from configparser import NoSectionError

from xml.etree import ElementTree as et


class PropertyFileUtil:
    @staticmethod
    def list_target_files(dir_path: str,
                          extension: str,
                          use_abstract_path: bool = True) -> List[str]:
        """
        列出指定扩展名的文件
        :param dir_path: 文件夹路径
        :param extension: 需要的扩展名
        :param use_abstract_path: 是否使用绝对路径
        :return: 符合要求的文件路径
        """
        file_name_list = os.listdir(dir_path)
        res = []
        for file_name in file_name_list:
            if os.path.isdir(file_name):
                continue
            file_extension = os.path.splitext(file_name)[1]
            if file_extension and extension == file_extension:
                if use_abstract_path:
                    fi_d = os.path.join(dir_path, file_name)
                else:
                    fi_d = file_name
                res.append(fi_d)

        return res

    @staticmethod
    def get_ini_data(file_path: str, item_name: str, encoding='utf-8') -> Dict[str, str]:
        """
        读取ini文件
        :param file_path: ini文件路径
        :param item_name: 要读取的块名称
        :param encoding: 文件编码方式
        :return:
        """
        return PropertyFileUtil.read_items_data(file_path, item_name, encoding)

    @staticmethod
    def read_items_data(
            file_path: str,
            item_name: str,
            encoding: str = 'utf-8') -> Dict[str, str]:
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

        # 读取csv文件

    @staticmethod
    def __get_csv_data(file_name: str, use_dict: bool = False):
        """
        
        :param file_name:
        :param use_dict:
        :return:
        """
        with open(file_name, newline='', encoding='utf-8') as f:
            if use_dict:
                reader = csv.DictReader(f)
            else:
                reader = csv.reader(f)

            return [i for i in reader]