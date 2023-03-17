from typing import List


def get_nest_degree_from_dict(d: dict) -> int:
    max_degree = 1
    for key in d:
        if isinstance(d[key], dict):
            sub_degree = get_nest_degree_from_dict(d[key])
            max_degree = max(max_degree, sub_degree + 1)

    return max_degree


def is_obj_iterable(obj: object) -> bool:
    """
    检查对象是否可迭代
    :param obj: 要检查的对象
    :return: 返回对象是否可迭代
    """
    try:
        iter(obj)
    except Exception as e:
        return False

    return True


if __name__ == '__main__':
    print(len(1))