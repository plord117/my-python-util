import copy

from typing import List, Any

import random

from algorithm.common.structure import TreeNode


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


def check_sort(sort_function,
               n: int,
               is_reverse: bool = True,
               show_detail: bool = False) -> None:
    """
    排序对数器
    :param sort_function: 自定义排序方法
    :param n: 测试册数
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

        if not check_two_array(array, copied_array):
            print("排序错误")
            raise ValueError("")


def check_two_array(arr1: List[Any], arr2: List[Any]) -> bool:
    """
    检查两个数组是否一致
    :param arr1: 数组1
    :param arr2: 数组2
    :return: 两个数组是否完全一致
    """
    return arr1 == arr2
