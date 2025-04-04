
import time
import os
import numpy as np

"""
Пример того, как работает `fork()` в POSIX системах. В данном случае под массив будет использоваться один блок физической памяти.
Структуру адрессоного пространства процесса можно посмотреть с помощью команды: 
    > pmap -X {pid}

pid - идентификатор процесса
"""

def main():
    big_array = np.zeros((100000, 10000))

    print(f'Pid: {os.getpid()}')

    # форкаем процесс
    if os.fork():   
        # родительский процесс
        print(f'Pid {os.getpid()}')
        if os.fork():
            print(f'Pid {os.getpid()}')
        else:
            print(f'Сhild #1 {os.getpid()}')
    else:
        # дочерний
        print(f'Сhild #2 {os.getpid()}')
        big_array[150] = 5

    time.sleep(100)

if __name__ == '__main__':
    main()