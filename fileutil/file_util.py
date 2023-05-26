import os

from typing import Dict, Generator, Optional, List, Any

from configparser import ConfigParser

import csv


import shutil
from shutil import ignore_patterns

from configparser import NoSectionError

from xml.etree import ElementTree as et

from xml.etree.ElementTree import Element


class FileUtil:
    @staticmethod
    def list_target_files(dir_path: str,
                          extension: str,
                          use_abstract_path: bool = True) -> Generator[str, None, None]:
        """
        列出指定扩展名的文件
        :param dir_path: 文件夹路径
        :param extension: 需要的扩展名
        :param use_abstract_path: 是否使用绝对路径
        :return: 符合要求的文件路径生成器
        """
        extension = extension if extension.startswith('.') else '.' + extension
        cwd = os.getcwd()

        for root, dir, files in os.walk(dir_path):
            for file in files:
                if file.endswith(extension):
                    full_name = os.path.join(root, file)
                    if use_abstract_path:
                        full_name = os.path.join(cwd, full_name)

                    yield full_name

    @staticmethod
    def copy_dir(src: str,
                 dst: str,
                 keep_signature: bool = False,
                 ignore: Optional[List[str]] = None) -> None:
        """
        复制文件夹
        :param src: 原地址
        :param dst: 目标地址
        :param keep_signature: 是否保留文件状态信息
        :param ignore: 忽略文件类型
        :return: None
        """
        if not os.path.exists(dst):
            if ignore is not None:
                temp_ignore = []
                for i in ignore:
                    if not i.startswith("*."):
                        if i.startswith('.'):
                            temp_ignore.append(f"*[{i}")
                        else:
                            temp_ignore.append(f"*.{i}")
                    else:
                        temp_ignore.append(f"{i}")
                ignore = ignore_patterns(*temp_ignore)
            shutil.copytree(src, dst, ignore=ignore)
        else:
            FileUtil.copy_files(src, dst, keep_signature, ignore)

    @staticmethod
    def copy_files(src: str,
                   dst: str,
                   keep_signature: bool,
                   ignore: Optional[List[str]]) -> None:
        """
        递归复制文件
        :param src: 原地址
        :param dst: 目标地址
        :param keep_signature: 是否保留文件状态信息
        :param ignore: 忽略文件类型
        :return: None
        """
        ignore_files = ignore if ignore is not None else []
        ignore_files = list(map(lambda a: f'.{a}' if not a.startswith('.') else a, ignore_files))
        copy_function = shutil.copy if keep_signature else shutil.copy2

        for file in os.listdir(src):
            new_src_path = os.path.join(src, file)
            if os.path.isdir(new_src_path):
                new_dst_path = os.path.join(dst, file)
                if not os.path.exists(new_dst_path):
                    os.mkdir(new_dst_path)
                FileUtil.copy_files(new_src_path, new_dst_path, keep_signature, ignore)
            else:
                src_file_path = os.path.join(src, file)
                dst_file_path = os.path.join(dst, file)
                if not os.path.exists(dst_file_path):
                    extension = os.path.splitext(src_file_path)[1]
                    if extension not in ignore_files:
                        copy_function(src_file_path, dst_file_path)


class PropertyFileUtil:
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
    def get_ini_parser(file_name: str, encoding: str) -> ConfigParser:
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
    def get_csv_data(file_name: str, use_dict: bool = False) -> List[List[str]]:
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

    @staticmethod
    def get_xml_data(file_path: str) -> dict[Element, dict[Any, Any]]:
        """
        获取xml配置信息
        :param file_path: xml文件路径
        :return: 配置参数字典
        """
        if os.path.splitext(file_path)[-1] != '.xml':
            raise TypeError("错误的文件类型")
        try:
            parser = et.parse(file_path)
        except Exception as e:
            raise e
        else:
            root_node = parser.getroot()
            res_dict = {root_node: {}}
            PropertyFileUtil.process_xml_data(root_node, res_dict[root_node])

            return res_dict

    @staticmethod
    def process_xml_data(node, dic) -> None:
        children = list(node)
        for child in children:
            if child not in dic:
                dic[child] = {}

            if list(child):
                PropertyFileUtil.process_xml_data(child, dic[child])
            else:
                dic[child][child.tag] = child.text
