"""
Enhance the efficiency of a hospital's patient records system by comparing the Bubble Sort and Merge Sort algorithms.

Algorithm: Bubble Sort and Merge Sort
Analyze the time complexity of both sorting algorithms
"""


import time

def merge_sort(list_data: list) -> list:
    """
    Takes a list of unsorted data, and sort it using the merge sort algorithm.
    :param list_data:
    :return:
    """
    # print(f"len(list_data): {len(list_data)}")
    if len(list_data) <= 1:
        return list_data

    mid = len(list_data) // 2
    left = list_data[:mid]
    right = list_data[mid:]

    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left, right)

def merge(left: list, right: list) -> list:
    """
    Merge two sorted lists into a single sorted list.
    :param left:
    :param right:
    :return:
    """
    result = []
    left_index, right_index = 0, 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:] + right[right_index:])
    return result

def bubble_sort(list_data: list) -> list:
    """
    Takes a list of unsorted data, and sort it using the bubble sort algorithm.
    :param list_data:
    :return:
    """
    arr =  list_data
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize: if no two elements were swapped
        # by inner loop, then break
        swapped = False

        # Last i elements are already in place
        for j in range(0, n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        # If no two elements were swapped by inner loop, then break
        if not swapped:
            break
    return arr

if __name__ == '__main__':
    import random

    int_list = random.sample(range(1, 3000), 2000)
    print(len(int_list))

    start_time = time.perf_counter()
    data = merge_sort(int_list)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(run_time)

    start_time = time.perf_counter()
    data = bubble_sort(int_list)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(run_time)

    # my_list =  [38, 27, 43, 3, 9, 82, 10, ]

    # print(data)
