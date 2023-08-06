from functools import wraps
from time import perf_counter
import sys

def isfloat(x):
    try:
        float(x)
        return True
    except:
        return False

def isstring(x):
    try:
        str(x)
        return True
    except:
        return False

def isint(x):
    try:
        int(x)
        return True
    except:
        return False

def radice(x):
    return x**.5


def get_time(func):

    def wrapper(*args, **kwargs):
        start_time = perf_counter()

        func(*args, *kwargs)

        end_time = perf_counter()

        total_time = round(end_time - start_time, 5)

        print('Durata:', total_time, 'secondi.')

    return wrapper

def setup():
    sys.setrecursionlimit(1000000000)
    print("Setup Done.")
    return "Setup Done. Recursion Limit Edited."

def optimize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]
    return wrapper

def timecalculator(start, end):
    return end-start

def fibonacci(x):
    if x < 2:
        return x
    return fibonacci(x-1) + fibonacci(x-2)

def isprime(x):
    flag = True
    for i in range(2, x):
        if (x % i) == 0:
            flag = False
            break

    return flag

if __name__ == '__main__':
    setup()

