from threading import Thread
from time import sleep

a: int = 0

def func_a():
    global a

    sleep(2)
    for _ in range(10000):
        a = 1

def func_b():
    global a 

    sleep(2)
    for _ in range(10000):
        a = 2

if __name__ == '__main__':
    t1 = Thread(target=func_a)
    t2 = Thread(target=func_b)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(a)