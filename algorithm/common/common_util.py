from typing import List, Any

import random

import string

from algorithm.common.structure import TreeNode

DEFAULT_LETTER = string.ascii_letters + string.digits


def swap(array: List[Any], i: int, j: int) -> None:
    """
    使用位运算加速交换数组
    :param array: 数组
    :param i: 索引1
    :param j: 索引2
    :return: None
    """
    if i == j:
        return

    array[i] = array[i] ^ array[j]
    array[j] = array[i] ^ array[j]
    array[i] = array[i] ^ array[j]


def get_random_string(length: int, base: str = DEFAULT_LETTER) -> str:
    """
    获取随机字符串
    :param length: 字符串长度
    :param base: 字符串基集合
    :return: 指定长度的字符串
    """
    salt = ''.join(random.sample(base, length))
    return salt


def get_random_substring(length: int, base: str):
    """

    :param length:
    :param base:
    :return:
    """
    base_length = len(base)
    start_index = random.randint(0, base_length - length - 1)

    return base[start_index: start_index + length]


def get_random_array(n: int, min_val: int = 0, max_val_int=100) -> List[int]:
    """
    获取随机数组
    :param n: 数组元素数量
    :param min_val: 数组最小值
    :param max_val_int: 数组最大值
    :return: 数组
    """
    return [random.randint(min_val, max_val_int) for _ in range(n)]


def get_random_tree(n: int) -> TreeNode:
    """
    获取随机二叉树
    :param n: 二叉树节点个数
    :return: 二叉树头结点
    """
    arr = get_random_array(n)
    return create_tree(arr)


def create_tree(arr) -> TreeNode:
    """
    根据数组创建二叉树
    :param arr: 数组
    :return: 二叉树头结点
    """
    return _create_tree_node(None, arr, 0)


def _create_tree_node(root, llist, i) -> TreeNode:
    if i < len(llist):
        if llist[i] == '#':
            return None
        else:
            root = TreeNode(llist[i])
            # 往左递推
            root.left = _create_tree_node(root.left, llist, 2 * i + 1)  # 从根开始一直到最左，直至为空，
            # 往右回溯
            root.right = _create_tree_node(root.right, llist, 2 * i + 2)  # 再返回上一个根，回溯右，

            return root
    return root
