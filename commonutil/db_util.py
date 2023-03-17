import pymysql

from pymysql.cursors import Cursor

from pymysql.connections import Connection


class DBUtil:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def re_connection(self):
        pass


