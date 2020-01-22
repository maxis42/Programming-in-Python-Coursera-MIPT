from concurrent.futures import ThreadPoolExecutor, as_completed


def f(a):
    return a * a


with ThreadPoolExecutor(max_workers=4) as pool:
    results = [pool.submit(f, i) for i in range(10000)]

    for future in as_completed(results):
        print(future.result())
