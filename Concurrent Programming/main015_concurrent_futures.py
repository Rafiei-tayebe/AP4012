# Another way to do the same as main008 using concurrent.futures
# concurrent.futures is imported to give us access to ThreadPoolExecutor
import concurrent.futures
import time


def do_something(seconds):
    print(f'Sleeping {seconds} second(s)...')
    time.sleep(seconds)
    return 'Done sleeping...'


if __name__ == '__main__':
    start = time.perf_counter()
    # A with statement is used to create a ThreadPoolExecutor instance executor
    # that will promptly clean up threads upon completion.
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(do_something, [1 for i in range(10)])

    for result in results:
        print(result)

    finish = time.perf_counter()
    print(f'Finished in {round(finish - start, 2)} second(s)')

