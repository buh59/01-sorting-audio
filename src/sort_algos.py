def bubble_sort(data):
    changed = 1
    while changed == 1:
        changed = 0
        for i in range(len(data) - 1):
            yield data, (i, i + 1)
            if data[i] > data[i + 1]:
                data[i], data[i + 1] = data[i + 1], data[i]
                changed = 1
                yield data, (i, i + 1)


def exchange_sort(data):
    n = len(data)
    for i in range(n - 1):
        for j in range(i + 1, n):
            yield data, (i, j)
            if data[i] > data[j]:
                data[i], data[j] = data[j], data[i]
                yield data, (i, j)


def selection_sort(data):
    n = len(data)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            yield data, (j, min_idx)
            if data[j] < data[min_idx]:
                min_idx = j
        if min_idx != i:
            data[i], data[min_idx] = data[min_idx], data[i]
            yield data, (i, min_idx)


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        yield arr, (i, j)
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            yield arr, (j, j + 1)
            j -= 1
        arr[j + 1] = key
        yield arr, (j + 1, i)


def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        yield arr, (j, high)
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
            yield arr, (i, j)
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr, (i + 1, high)
    return i + 1


def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = yield from partition(arr, low, high)
        yield from quick_sort(arr, low, pi - 1)
        yield from quick_sort(arr, pi + 1, high)


def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n:
        yield arr, (l, largest)
        if arr[l] > arr[largest]:
            largest = l

    if r < n:
        yield arr, (r, largest)
        if arr[r] > arr[largest]:
            largest = r

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        yield arr, (i, largest)
        yield from heapify(arr, n, largest)


def heap_sort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, (0, i)
        yield from heapify(arr, i, 0)
