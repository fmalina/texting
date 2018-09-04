"""Prototype for parallel sending of texts.

Uses multiple GSM modems at once.
"""

from multiprocessing import Process


def parallel(target_func, args_ls):
    proc = []
    for args in args_ls:
        p = Process(target=target_func, args=args)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


if __name__ == '__main__':
    import time
    import random

    def test(modem, numbers):
        for no in numbers:
            r = random.random()
            time.sleep(no * r)
            print(modem, no, '*', r)
        print('FINISHED', modem)
    
    tests = (
        ('A', (1, 2, 3)),
        ('B', (1, 2, 3)),
        ('C', (1, 2, 3))
    )
    parallel(test, tests)
