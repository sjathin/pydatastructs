from pydatastructs import (
    merge_sort_parallel, DynamicOneDimensionalArray,
    OneDimensionalArray, brick_sort, brick_sort_parallel,
    heapsort, matrix_multiply_parallel, counting_sort, bucket_sort, cocktail_shaker_sort, quick_sort, longest_common_subsequence,
    is_ordered, upper_bound, lower_bound)

from pydatastructs.utils.raises_util import raises
import random

def _test_common_sort(sort, *args, **kwargs):
    random.seed(1000)

    n = random.randint(10, 20)
    arr = DynamicOneDimensionalArray(int, 0)
    for _ in range(n):
        arr.append(random.randint(1, 1000))
    for _ in range(n//3):
        arr.delete(random.randint(0, n//2))
    expected_arr = [686, 779, 102, 134, 362, 448,
                    480, 548, None, None, None,
                    228, 688, 247, 373, 696, None,
                    None, None, None, None, None,
                    None, None, None, None, None,
                    None, None, None, None]
    sort(arr, *args, **kwargs, start=2, end=10)
    assert arr._data == expected_arr
    sort(arr, *args, **kwargs)
    expected_arr = [102, 134, 228, 247, 362, 373, 448,
                    480, 548, 686, 688, 696, 779,
                    None, None, None, None, None, None,
                    None, None, None, None, None,
                    None, None, None, None, None, None, None]
    assert arr._data == expected_arr
    assert (arr._last_pos_filled, arr._num, arr._size) == (12, 13, 31)

    n = random.randint(10, 20)
    arr = OneDimensionalArray(int, n)
    for i in range(n):
        arr[i] = random.randint(1, 1000)
    expected_arr = [42, 695, 147, 500, 768,
                    998, 473, 732, 728, 426,
                    709, 910]
    sort(arr, *args, **kwargs, start=2, end=5)
    assert arr._data == expected_arr

def test_merge_sort_parallel():
    _test_common_sort(merge_sort_parallel, num_threads=5)

def test_brick_sort():
    _test_common_sort(brick_sort)

def test_brick_sort_parallel():
    _test_common_sort(brick_sort_parallel, num_threads=3)

def test_heapsort():
    _test_common_sort(heapsort)

def test_bucket_sort():
    _test_common_sort(bucket_sort)

def test_counting_sort():
    random.seed(1000)

    n = random.randint(10, 20)
    arr = DynamicOneDimensionalArray(int, 0)
    for _ in range(n):
        arr.append(random.randint(1, 1000))
    for _ in range(n//3):
        arr.delete(random.randint(0, n//2))

    expected_arr = [102, 134, 228, 247, 362, 373, 448,
                    480, 548, 686, 688, 696, 779]
    assert counting_sort(arr)._data == expected_arr

def test_cocktail_shaker_sort():
    _test_common_sort(cocktail_shaker_sort)

def test_quick_sort():
    _test_common_sort(quick_sort)

def test_matrix_multiply_parallel():
    ODA = OneDimensionalArray

    expected_result = [[3, 3, 3], [1, 2, 1], [2, 2, 2]]

    I = ODA(ODA, [ODA(int, [1, 1, 0]), ODA(int, [0, 1, 0]), ODA(int, [0, 0, 1])])
    J = ODA(ODA, [ODA(int, [2, 1, 2]), ODA(int, [1, 2, 1]), ODA(int, [2, 2, 2])])
    output = matrix_multiply_parallel(I, J, num_threads=5)
    assert expected_result == output

    I = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    output = matrix_multiply_parallel(I, J, num_threads=5)
    assert expected_result == output

    I = [[1, 1, 0, 1], [0, 1, 0, 1], [0, 0, 1, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    assert raises(ValueError, lambda: matrix_multiply_parallel(I, J, num_threads=5))

    I = [[1, 1, 0], [0, 1, 0], [0, 0, 1]]
    J = [[2, 1, 2], [1, 2, 1], [2, 2, 2]]
    output = matrix_multiply_parallel(I, J, num_threads=1)
    assert expected_result == output

def test_longest_common_sequence():
    ODA = OneDimensionalArray
    expected_result = "['A', 'S', 'C', 'I', 'I']"

    str1 = ODA(str, ['A', 'A', 'S', 'C', 'C', 'I', 'I'])
    str2 = ODA(str, ['A', 'S', 'S', 'C', 'I', 'I', 'I', 'I'])
    output = longest_common_subsequence(str1, str2)
    assert str(output) == expected_result

    expected_result = "['O', 'V', 'A']"

    I = ODA(str, ['O', 'V', 'A', 'L'])
    J = ODA(str, ['F', 'O', 'R', 'V', 'A', 'E', 'W'])
    output = longest_common_subsequence(I, J)
    assert str(output) == expected_result

    X = ODA(int, [1, 2, 3, 4, 5, 6, 6, 5, 4, 3, 2, 1])
    Y = ODA(int, [1, 2, 3, 4, 4, 3, 2, 1])
    output = longest_common_subsequence(X, Y)
    assert str(output) == '[1, 2, 3, 4, 4, 3, 2, 1]'

    Z = ODA(int, [])
    output = longest_common_subsequence(Y, Z)
    assert str(output) == '[]'

def test_is_ordered():
    ODA = OneDimensionalArray
    DODA = DynamicOneDimensionalArray

    expected_result = True
    arr = ODA(int, [1, 2, 5, 6])
    output = is_ordered(arr)
    assert output == expected_result

    expected_result = False
    arr1 = ODA(int, [4, 3, 2, 1])
    output = is_ordered(arr1)
    assert output == expected_result

    expected_result = True
    arr2 = ODA(int, [6, 1, 2, 3, 4, 5])
    output = is_ordered(arr2, start=1, end=5)
    assert output == expected_result

    expected_result = True
    arr3 = ODA(int, [0, -1, -2, -3, -4, 4])
    output = is_ordered(arr3, start=1, end=4, comp=lambda u, v: u > v)
    assert output == expected_result

    expected_result = True
    arr4 = DODA(int, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    arr4.delete(0)
    output = is_ordered(arr4)
    assert output == expected_result

def test_upper_bound():
    ODA = OneDimensionalArray
    arr1 = ODA(int, [3, 3, 3])
    output = upper_bound(arr1, 3)
    expected_result = 3
    assert expected_result == output

    arr2 = ODA(int, [4, 4, 5, 6])
    output = upper_bound(arr2, 4, end=3)
    expected_result = 2
    assert expected_result == output

    arr3 = ODA(int, [6, 6, 7, 8, 9])
    output = upper_bound(arr3, 5, start=2, end=4)
    expected_result = 2
    assert expected_result == output

    arr4 = ODA(int, [3, 4, 4, 6])
    output = upper_bound(arr4, 5, start=1, end=3)
    expected_result = 3
    assert expected_result == output

    arr5 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = upper_bound(arr5, 6, comp=lambda x, y: x > y)
    expected_result = 5
    assert expected_result == output

    arr6 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = upper_bound(arr6, 2, start=2, comp=lambda x, y: x > y)
    expected_result = 8
    assert expected_result == output

    arr7 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = upper_bound(arr7, 9, start=3, end=7, comp=lambda x, y: x > y)
    expected_result = 3
    assert expected_result == output

    arr8 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = upper_bound(arr8, 6, end=3, comp=lambda x, y: x > y)
    expected_result = 3
    assert expected_result == output


def test_lower_bound():
    ODA = OneDimensionalArray
    arr1 = ODA(int, [3, 3, 3])
    output = lower_bound(arr1, 3, start=1)
    expected_result = 1
    assert expected_result == output

    arr2 = ODA(int, [4, 4, 4, 4, 5, 6])
    output = lower_bound(arr2, 5, end=3)
    expected_result = 3
    assert expected_result == output

    arr3 = ODA(int, [6, 6, 7, 8, 9])
    output = lower_bound(arr3, 5, end=3)
    expected_result = 0
    assert expected_result == output

    arr4 = ODA(int, [3, 4, 4, 4])
    output = lower_bound(arr4, 5)
    expected_result = 4
    assert expected_result == output

    arr5 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = lower_bound(arr5, 5, comp=lambda x, y: x > y)
    expected_result = 5
    assert expected_result == output

    arr6 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = lower_bound(arr6, 2, start=4, comp=lambda x, y: x > y)
    expected_result = 8
    assert expected_result == output

    arr7 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = lower_bound(arr7, 9, end=5, comp=lambda x, y: x > y)
    expected_result = 0
    assert expected_result == output

    arr8 = ODA(int, [7, 6, 6, 6, 6, 5, 4, 3])
    output = lower_bound(arr8, 6, end=3, comp=lambda x, y: x > y)
    expected_result = 1
    assert expected_result == output
