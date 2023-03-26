from typing import List

from operator import gt, lt

import sys

from algorithm.common.common_util import swap

__all__ = ["radix_sort", "shell_sort", "heap_sort", "quick_sort",
           "merge_sort", "bubble_sort", "insert_sort", "selection_sort"]


def merge_sort(array: List[int], reverse: bool = False) -> None:
    """
    归并排序
    :param array: 要排序的列表
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    _merge_sort(array, 0, len(array) - 1, reverse)


def _merge_sort(array: List[int], left_index: int, right_index: int, reverse: bool) -> None:
    if left_index == right_index:
        return

    mid_index = left_index + ((right_index - left_index) >> 1)
    _merge_sort(array, left_index, mid_index, reverse)
    _merge_sort(array, mid_index + 1, right_index, reverse)
    _merge_array(array, left_index, mid_index, right_index, reverse)


def _merge_array(array: List[int], left_index: int, mid_index: int, right_index: int, reverse: bool):
    i = 0
    help_array = [0] * (right_index - left_index + 1)
    counter1 = left_index
    counter2 = mid_index + 1
    cmp_operator = __get_cmp_operator(reverse)

    while counter1 <= mid_index and counter2 <= right_index:
        if cmp_operator(array[counter1], array[counter2]):
            help_array[i] = array[counter1]
            counter1 += 1
        else:
            help_array[i] = array[counter2]
            counter2 += 1
        i += 1

    while counter1 <= mid_index:
        help_array[i] = array[counter1]
        counter1 += 1
        i += 1

    while counter2 <= right_index:
        help_array[i] = array[counter2]
        counter2 += 1
        i += 1

    for i, v in enumerate(help_array):
        array[left_index + i] = v


def bubble_sort(array: List[int], reverse: bool = False) -> None:
    """
    冒泡排序
    :param array: 要排序的列表
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    length = len(array)
    cmp_operator = __get_cmp_operator(reverse)

    for i in range(0, length):
        for j in range(1, length - i):
            if cmp_operator(array[j], array[j - 1]):
                swap(array, j, j - 1)


def insert_sort(array: List[int], reverse: bool = False) -> None:
    """
    插入排序
    :param array: 要排序的列表
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    length = len(array)
    cmp_operator = __get_cmp_operator(reverse)

    for i in range(1, length):
        for j in range(i, 0, -1):
            if cmp_operator(array[j], array[j - 1]):
                swap(array, j, j - 1)
            else:
                break


def selection_sort(array: List[int], reverse: bool = False) -> None:
    """
    选择排序
    :param array: 要排序的数组
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    length = len(array)
    cmp_operator = __get_cmp_operator(reverse)

    for i in range(length):
        cmp_val = min(array) - 1 if reverse else sys.maxsize
        swap_index = 0
        for j in range(i, length):
            if cmp_operator(array[j], cmp_val):
                swap_index = j
                cmp_val = array[j]

        swap(array, i, swap_index)


def quick_sort(array: List[int], reverse: bool = False) -> None:
    """
    快速排序
    :param array: 要排序的数组
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    length = len(array)
    _quick_sort(array, 0, length - 1, reverse)


def _quick_sort(array: List[int], left_index: int, right_index: int, reverse: bool) -> None:
    if left_index < right_index:
        pi = _partition(array, left_index, right_index, reverse)

        _quick_sort(array, left_index, pi - 1, reverse)
        _quick_sort(array, pi + 1, right_index, reverse)


def _partition(array: List[int], left_index: int, right_index: int, reverse: bool) -> int:
    i = (left_index - 1)
    pivot = array[right_index]
    cmp_operator = __get_cmp_operator(reverse)

    for j in range(left_index, right_index):
        if cmp_operator(array[j], pivot):
            i = i + 1
            array[i], array[j] = array[j], array[i]

    array[i + 1], array[right_index] = array[right_index], array[i + 1]
    return i + 1


def heap_sort(array: List[int], reverse: bool = False) -> None:
    """
    堆排序
    :param array: 要排序的数组
    :param reverse: 是否降序
    :return: None
    """
    if not array or len(array) <= 2:
        return

    length = len(array)

    for i in range(length):
        _flow(array, i, reverse)

    while length > 0:
        length -= 1
        swap(array, 0, length)
        _sink(array, 0, length, reverse)


def _sink(array: List[int], index: int, max_size: int, reverse: bool) -> None:
    left_child_index = 2 * index + 1
    cmp_operator = __get_cmp_operator(reverse)

    while left_child_index < max_size:
        right_child_index = left_child_index + 1 if left_child_index + 1 < max_size else left_child_index
        if reverse:
            cmp_index = left_child_index if array[left_child_index] < array[right_child_index] else right_child_index
        else:
            cmp_index = left_child_index if array[left_child_index] > array[right_child_index] else right_child_index

        if cmp_operator(array[index], array[cmp_index]):
            swap(array, index, cmp_index)
            index = cmp_index
            left_child_index = 2 * index + 1
        else:
            break


def _flow(array: List[int], index: int, reverse: bool) -> None:
    father_index = (index - 1) >> 1
    cmp_operator = __get_cmp_operator(not reverse)
    while father_index >= 0:
        if cmp_operator(array[index], array[father_index]):
            swap(array, index, father_index)
            index = father_index
            father_index = (index - 1) >> 1
        else:
            break


def shell_sort(array: List[int], reverse: bool = False):
    """
    希尔排序
    :param array: 要排序的数组
    :param reverse:
    :return:
    """
    n = len(array)
    gap = int(n / 2)
    cmp_operator = __get_cmp_operator(not reverse)

    while gap > 0:

        for i in range(gap, n):

            temp = array[i]
            j = i
            while j >= gap and cmp_operator(array[j - gap], temp):
                array[j] = array[j - gap]
                j -= gap
            array[j] = temp
        gap = int(gap / 2)


def radix_sort(arr: List[int], reverse: bool = False):
    n = len(str(max(arr)))
    for k in range(n):
        bucket_list = [[] for _ in range(10)]
        for i in arr:
            bucket_list[i // (10 ** k) % 10].append(i)
        arr = [j for i in bucket_list for j in i]
    return arr[::-1] if reverse else arr


def __get_cmp_operator(reverse):
    """
    获取比较符号
    :param reverse: 是否降序
    :return: function 是否降序
    """
    return gt if reverse else lt
