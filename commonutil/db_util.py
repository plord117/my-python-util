from typing import Dict, Optional

import json, os

import pymysql

from pymysql.cursors import Cursor

from pymysql.connections import Connection

from fileutil.file_util import PropertyFileUtil


class MyDatabase:
    def __init__(self, host=None, user=None, db=None, pwd=None, port=None):
        self.connection: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None

        self.host = host
        self.user = user
        self.db = db
        self.pwd = pwd
        self.port = port
        self.connection_flg = False

    @staticmethod
    def get_connection_from_dict(param_dict: Dict):
        """
        从字典获取MyDatabase
        :param param_dict: 配置参数字典
        :return: MyDatabase对象
        """
        host = param_dict.get("host", None)
        user = param_dict.get("user", None)
        pwd = param_dict.get("password", None)
        db = param_dict.get("database", None)
        port = int(param_dict.get("port", None))

        db = MyDatabase(host, user, db, pwd, port)

        return db

    @staticmethod
    def get_db_from_json(params: str):
        """
        从json中获取MyDatabase对象
        :param params: json字符串
        :return: MyDatabase对象
        """
        params_dict = json.load(params)
        return MyDatabase.get_connection_from_dict(params_dict)

    @staticmethod
    def get_db_from_properties(file_path: str):
        """
        从ini配置文件中获取数据库连接
        :param file_path: ini文件路径
        :return: MyDatabase对象
        """
        if not os.path.exists(file_path):
            raise OSError(f"配置文件{file_path}不存在")

        params_dict = PropertyFileUtil.get_ini_data(file_path, "PROPERTY")
        return MyDatabase.get_connection_from_dict(params_dict)

    def close_db(self) -> None:
        """
        关闭连接
        :return: None
        """
        self.cursor.close()
        self.connection.close()

        self.connection = None
        self.cursor = None
        self.connection_flg = False

    def connect_db(self) -> None:
        """
        连接数据库
        :return: None
        """
        if self.host is not None \
                and self.db is not None \
                and self.user is not None \
                and self.port is not None \
                and self.port is not None:

            try:
                self.connection = pymysql.connect(host=self.host,
                                                  user=self.user,
                                                  password=self.pwd,
                                                  database=self.db,
                                                  port=self.port)

                self.cursor = self.connection.cursor()
            except Exception as e:
                print(e)
                self.connection_flg = False
            else:
                self.connection_flg = True

    def execute_sql(self, sql: str, is_commit: bool = False) -> int:
        """
        执行SQL
        :param sql: 要执行的SQL语句
        :param is_commit: 是否提交
        :return: 受到影响的数据条数
        """
        if not self.connection_flg:
            raise RuntimeError("没有完成连接")
        try:
            effected_row = self.cursor.execute(sql)
        except Exception as e:
            self.connection.rollback()
        else:
            if is_commit:
                self.connection.commit()

            return effected_row
