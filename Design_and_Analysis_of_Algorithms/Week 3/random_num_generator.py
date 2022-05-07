"""
Description: The program performs sorts on lists of random numbers using four different algorithms
and prints their respective execution speeds.
"""

import time
import random

def main():

    def selection_sort(arr):
        for i in range(len(arr)):
            min_idx = i
            for j in range(i+1, len(arr)):
                if arr[min_idx] > arr[j]:
                    min_idx = j 
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    def insertion_sort(arr):
        for i in range(1, len(arr)):
            elem = arr[i]
            j = i-1
            while j >=0 and elem < arr[j] :
                    arr[j+1] = arr[j]
                    j -= 1
            arr[j+1] = elem

    def quicksort(arr):
        if len(arr) <= 1: return arr 
        pivot = random.choice(arr)
        lt, eq, gt = [], [], [] 
        for val in arr: 
            if val < pivot: lt.append(val)
            elif val > pivot: gt.append(val)
            else: eq.append(val)
        return quicksort(lt) + eq + quicksort(gt) 

    def merge(arr1, arr2):
        res = []
        i, j = 0, 0
        while i < len(arr1) and j < len(arr2): 
            if arr1[i] <= arr2[j]:
                res.append(arr1[i])
                i += 1
            else:
                res.append(arr2[j])
                j += 1

        if i < len(arr1):
            res += arr1[i:]
        if j < len(arr2):
            res += arr2[j:]
        return res

    def merge_sort(arr): 
        if len(arr) == 1: return arr
        mid = len(arr)//2
        L = merge_sort(arr[:mid])
        R = merge_sort(arr[mid:])
        return merge(L, R) 

    # Selection sort
    rand_list1 = random.sample(range(0, 1000), 500)
    t1_start = time.perf_counter()
    selection_sort(rand_list1)
    t1_stop = time.perf_counter()
    print(f"Selection sort time: {t1_stop - t1_start:.6f} seconds")

    # Insertion sort
    rand_list2 = random.sample(range(0, 1000), 500)
    t2_start = time.perf_counter()
    insertion_sort(rand_list2)
    t2_stop = time.perf_counter()
    print(f"Insertion sort time: {t2_stop - t2_start:.6f} seconds")

    # Quicksort
    rand_list3 = random.sample(range(0, 1000), 500)
    t3_start = time.perf_counter()
    quicksort(rand_list3)
    t3_stop = time.perf_counter()
    print(f"Quicksort time: {t3_stop - t3_start:.6f} seconds")

    # Merge sort
    rand_list4 = random.sample(range(0, 1000), 500)
    t4_start = time.perf_counter()
    merge_sort(rand_list4)
    t4_stop = time.perf_counter()
    print(f"Merge sort time: {t4_stop - t4_start:.6f} seconds")

if __name__ == "__main__":
    main()
