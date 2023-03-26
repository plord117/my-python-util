import copy
import time
from algorithm.common.common_util import check_sort
from algorithm.common.common_util import get_random_array
from algorithm.sort import merge_sort, bubble_sort, insert_sort, selection_sort, quick_sort, heap_sort, shell_sort, radix_sort

reverse = True
sort_test_function = quick_sort
N = 10
check_sort(sort_test_function, N, show_detail=True, is_reverse=reverse)
time.sleep(2)
reverse = not reverse
check_sort(sort_test_function, N, show_detail=True, is_reverse=reverse)


for _ in range(10):
    arr = get_random_array(15)
    na = copy.deepcopy(arr)
    na.sort(reverse=reverse)
    arr = radix_sort(arr, reverse=reverse)
    print(na == arr)