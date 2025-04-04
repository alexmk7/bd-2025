import os

from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection

"""
    Pipe - механизм межпроцессорорного взаимодействия, по сути - двунаправленный канал. Сообщения, передаваемые через Pipe, 
    должны поддерживать сериализацию через pickle
"""

# Процесс
def process(conn: Connection):
    # выводим на экран pid
    print(f'Child pid: {os.getpid()}')

    while True:
        # получаем сообщение (ждем, пока его нет)
        val = conn.recv()
        # если None - выходим и завершаем процесс
        if val == None:
            return

        # шлем в Connection число умноженное на два
        conn.send(val * 2)

def main():
    print(f'Parent pid: {os.getpid()}')
    # создаем Pipe (один 'выход' для родительского процесса, другой для дочернего)
    conn_parent, conn_child = Pipe()

    # запускаем процесс
    proc = Process(target=process, args=(conn_child,))
    proc.start()

    # шлем сообщения
    for idx in range(10):        
        print(f'Send {idx}')
        conn_parent.send(idx)
        
        ret = conn_parent.recv()
        print(f'Recieved {ret}')
    
    # посылаем None, чтобы процесс завершился
    conn_parent.send(None)
        

if __name__ == '__main__':
    main()
