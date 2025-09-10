from typing import Union, List

Number = Union[int, float, complex]


def find_insert_position(array: List[Number], number: Number) -> int:
    start  = 0
    end = len(array) - 1
    if len(array) == 0:
        return 0
    elif number > array[end]:
        return end + 1
    while start < end:
        middle = int(start + (end - start) / 2)
        if array[middle] == number:
            return middle
        elif array[middle] < number:
            start = middle + 1
        else:
            end = middle
    return start

if __name__ == '__main__':
    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    insert_position: int = find_insert_position(A, x)
    assert insert_position == 5

    A: List[Number] = [1, 2, 3, 3, 3, 5]
    x: Number = 4
    A.insert(insert_position, x)
    assert A == sorted(A)
