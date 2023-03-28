from typing import List

__all__ = ["sunday_substring_search", "binary_search", "kmp_substring_search", "force_substring_search"]


def binary_search(array: List[int], target: int) -> int:
    """
    二分搜索
    :param array: 要搜索的数组
    :param target: 要搜索的数字
    :return: 数字所在的索引
    """
    array.sort()

    left_index = 0
    right_index = len(array) - 1

    while left_index <= right_index:
        mid_index = left_index + int(((right_index - left_index) >> 1))
        mid_value = array[mid_index]
        if mid_value == target:
            return mid_index
        else:
            if mid_value < target:
                left_index = mid_index + 1
            else:
                right_index = mid_index - 1

    return -1


def force_substring_search(txt: str, pat: str) -> int:
    """
    暴力字符串匹配
    :param txt: 原始字符串
    :param pat: 模式字符串
    :return: 匹配起始点
    """
    txt_length = len(txt)
    pat_length = len(pat)

    for i in range(0, txt_length - pat_length):
        for j in range(0, pat_length):
            if pat[j] != txt[i + j]:
                break
            else:
                if j == pat_length - 1:
                    return i

    return -1


def sunday_substring_search(txt, pat):
    """
    sunday算法
    :param txt: 主串
    :param pat: 模式串
    :return: 返回第一个匹配到模式串中第一个字符在主串中的下标
    """
    m, f = 0, 0
    m_len, f_len = len(txt), len(pat)
    while m < m_len:
        if txt[m] == pat[f]:
            m, f = m + 1, f + 1
            if f == f_len:
                return m - f_len  # 此时找到了第一个匹配到的下标
            continue
        else:
            flag = m - f + f_len
            if flag > m_len - 1:  # main_str下标越界，没有找到匹配的串
                return -1
            check_exits = pat.rfind(txt[flag])
            if check_exits != -1:  # 在find_str中有匹配
                jump = f_len - check_exits  # 移动的步长
                m, f = m - f + jump, 0
            else:  # 在find_str中无匹配
                jump = f_len + 1  # 移动的步长
                m, f = m - f + jump, 0
    else:
        return -1


def kmp_substring_search(txt, pat):
    """
    kmp算法
    :param txt: 原始字符串
    :param pat: 模式字符串
    :return: 搜索的位置
    """
    nex = _get_next(pat)
    i = 0
    j = 0
    while i < len(txt) and j < len(pat):
        if j == -1 or txt[i] == pat[j]:
            i += 1
            j += 1
        else:
            j = nex[j]

    if j == len(pat):
        return i - j
    else:
        return -1


def _get_next(pat):
    nex = [0] * (len(pat) + 1)
    nex[0] = -1
    i = 0
    j = -1
    while i < len(pat):
        if j == -1 or pat[i] == pat[j]:
            i += 1
            j += 1
            nex[i] = j
        else:
            j = nex[j]

    return nex
