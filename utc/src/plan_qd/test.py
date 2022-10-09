import numpy as np
from multiprocessing import Pool
import time


def func1(x, y=1):
    time.sleep(0.1)
    return x ** 2 + y


def func2(n, parallel=False):
    my_array = np.zeros((n))

    # Parallelized version:
    if parallel:
        pool = Pool(processes=6)
        ####### HERE COMES THE CHANGE #######
        results = [pool.apply_async(func1, [val]) for val in range(1, n + 1)]
        for idx, val in enumerate(results):
            my_array[idx] = val.get()
        #######
        pool.close()

    # Not parallelized version:
    else:
        for i in range(1, n + 1):
            my_array[i - 1] = func1(i)

    return my_array


def main():
    start = time.time()
    my_array = func2(600)
    end = time.time()

    print(my_array)
    print("Normal time: {}\n".format(end - start))

    start_parallel = time.time()
    my_array_parallelized = func2(600, parallel=True)
    end_parallel = time.time()

    print(my_array_parallelized)
    print("Time based on multiprocessing: {}".format(end_parallel - start_parallel))


if __name__ == '__main__':
    main()