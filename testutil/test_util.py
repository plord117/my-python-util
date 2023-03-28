import copy, time

import random

from typing import List, Any

from algorithm.common.common_util import get_random_array, get_random_substring, get_random_string

__all__ = ["check_val_search_func", "check_substring_search_func", "check_sort"]


def check_sort(sort_function,
               n: int,
               show_detail: bool = False) -> None:
    """
    排序对数器包装方法，可以快速检测自己的排序函数
    :param sort_function: 自定义排序方法
    :param n: 测试次数
    :param show_detail: 是否显示排序细节
    :return: None
    """
    _check_sort(sort_function, n, is_reverse=True, show_detail=show_detail)
    time.sleep(2)
    _check_sort(sort_function, n, is_reverse=False, show_detail=show_detail)


def _check_sort(sort_function,
                n: int,
                is_reverse: bool = False,
                show_detail: bool = False) -> None:
    """
    排序对数器
    :param sort_function: 自定义排序方法
    :param n: 测试次数
    :param is_reverse: 是否逆序
    :param show_detail: 是否显示排序细节
    :return: None
    """
    for _ in range(n):
        array = get_random_array(15)
        copied_array = copy.deepcopy(array)

        copied_array.sort(reverse=is_reverse)
        sort_function(array, reverse=is_reverse)

        if show_detail:
            print(f"*** 第{_ + 1}次测试 ***")
            print(f"系统排序：{copied_array}")
            print(f"您的排序: {array}")
            print("")

        if not _check_two_array(array, copied_array):
            raise ValueError("排序错误")

    print(f"总计{n}次测试完成，全部正确")


def _check_two_array(arr1: List[Any], arr2: List[Any]) -> bool:
    """
    检查两个数组是否一致
    :param arr1: 数组1
    :param arr2: 数组2
    :return: 两个数组是否完全一致
    """
    return arr1 == arr2


def check_substring_search_func(search_function,
                                n: int,
                                base_length: int = 15,
                                substring_length: int = 5,
                                show_detail: bool = False) -> None:
    """
    字符串搜索
    :param search_function:
    :param n:
    :param base_length:
    :param substring_length:
    :param show_detail:
    :return:
    """
    for _ in range(n):
        base = get_random_string(base_length)
        substring = get_random_substring(substring_length, base)

        start_index = search_function(base, substring)

        if show_detail:
            print(f"*** 第{_ + 1}次测试 ***")
            print(f"base串：{base}")
            print(f"要搜索的子串：{substring}")
            print(f"搜索算法返回的结果是：{start_index}")
            print(f"根据返回索引和子串长度，您的搜索结果是：{base[start_index: start_index + substring_length]}")
            print("")

        if not base[start_index: start_index + substring_length] == substring:
            raise ValueError("字符串子串搜索错误")

    print(f"总计{n}次测试完成，全部正确")


def check_val_search_func(func, n: int, show_detail: bool = False) -> None:
    """
    数组搜索方法测试
    :param func: 数字搜索方法
    :param n: 测试轮数
    :param show_detail: 是否显示细节
    :return: None
    """
    for _ in range(n):
        array = get_random_array(15)
        target = random.choice(array + [-1, 101])
        index = func(array, target)

        if show_detail:
            print(f"要搜索的数组是：{array}")
            print(f"要搜索的数字是：{target}")
            print(f"您得搜索算法给出的结果是：{index}")
            print(f"")

        if (target in array and array[index] != target) or (target not in array and index != -1):
            raise ValueError("搜索算法错误")

    print(f"总计{n}次测试完成，全部正确")
