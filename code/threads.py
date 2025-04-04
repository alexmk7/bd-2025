
import time
import threading

"""
    Запускаем потоки на Python
"""


# Функция потока
def foo(n: int, thread_num: int):
    res = 1
    for i in range(1, n + 1):
        res *= i
        
    print('Thread {}: {}\n'.format(thread_num, res))

    time.sleep(15)


def main():
    # создаем объекты потоков
    thread1 = threading.Thread(target=foo, args=(5, 1))
    thread2 = threading.Thread(target=foo, args=(25, 2))

    # запускаем
    thread1.start()
    thread2.start()

    # ждем завершения
    thread1.join()
    thread2.join()


if __name__ == '__main__':
    main()
