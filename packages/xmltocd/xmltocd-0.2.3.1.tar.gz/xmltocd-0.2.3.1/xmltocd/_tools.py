from typing import List
from functools import reduce

def __intersection(obj1, obj2):
    result = []
    for _1 in obj1:
        for _2 in obj2:
            if _1 == _2:
                result.append(_1)
                break
    return result

def find_intersection(datas: List[List[int]]) -> List[int]:
    return list(reduce(__intersection, datas))
