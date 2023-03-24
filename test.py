from algorithm.common.common_util import check_sort

def my_sort(a:[], reverse):
    a.sort(reverse=reverse)

f = my_sort

check_sort(f, 10000, show_detail=True)