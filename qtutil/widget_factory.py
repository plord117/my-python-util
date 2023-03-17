from typing import List

from enum import Enum, unique

from PyQt5.QtWidgets import QCompleter, QDirModel

from PyQt5.QtCore import QTimer, QStringListModel, Qt, QRegExp

from PyQt5.QtGui import QRegExpValidator


@unique
class NormalReg(Enum):
    ONLY_UPPER_CASE = "^[A-Z]+$"
    ONLY_LOWER_CASE = "^[a-z]+$"
    ONLY_DIGIT_NUMBER = "^[0-9]+$"
    USER_NAME = "^[0-9A-Za-z_]+$"


# 获取计时器
def get_timer(slot, is_single: bool = False) -> QTimer:
    """
    获取计时器对象

    :param slot: 计时器绑定的槽函数对象
    :param is_single: 指定是否是单触发
    :return: QTimer对象
    """
    timer = QTimer()
    timer.timeout.connect(slot)
    timer.setSingleShot(is_single)

    return timer


def get_dir_completer() -> QCompleter:
    """
    获取输入框路径自动补全
    :return: QCompleter对象
    """
    dir_model = QDirModel()
    completer = QCompleter()
    completer.setModel(dir_model)

    return completer


def get_list_completer(str_list: List[str],
                       case_sensitive: bool = False,
                       max_items: int = 7) -> QCompleter:
    """
    要设置的字符串列表补全器

    :param str_list: 要设置的补全列表
    :param case_sensitive: 指定对大小写是否敏感
    :param max_items: 指定最大的可见提示数目
    :return: QCompleter对象
    """
    completer = QCompleter()
    model = QStringListModel(str_list)
    completer.setModel(model)
    completer.setMaxVisibleItems(max_items)
    # 设置是否大小写敏感
    completer.setCaseSensitivity(Qt.CaseSensitive if case_sensitive else Qt.CaseInsensitive)

    return completer


# 获取正则表达式输入限制器
def get_regression_validator(regression: str, normal_type: NormalReg = None) -> QRegExpValidator:
    """
    返回一个正则输入限制器

    :param regression: 正则表达式的值
    :param normal_type: 常用表达式类型
    :return: QRegExpValidator
    """
    assert isinstance(regression, str)

    # 获得正则表达式的QRegExp对象
    reg = QRegExp(regression)
    # 获得正则输入限制器
    validator = QRegExpValidator(reg)

    return validator
