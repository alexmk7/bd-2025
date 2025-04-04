import mmap
import os
from timeit import default_timer
import random
from contextlib import contextmanager

import numpy as np

@contextmanager
def temp_file(f_name: str, num_words: int=100):
    """
    Контекстный менеджер - создает файл, заполняет его случайными словами, удаляет за собой
    """  
    alpha = [chr(ch) for ch in range(ord('a'), ord('z')+1)]    

    try:
        with open(f_name, "w") as f:
            for _ in range(num_words):
                random_word = ''.join(random.choices(alpha, k=random.randint(2, 10)))
                f.write(random_word)
                f.write(" ")

        yield f_name            
    finally:        
        os.remove(f_name)


def read_file(f_name: str, num_first_symbols: int=10) -> str:    
    """
    Читает содержимое текстового файла и возвращает первые `num_first_symbols` символов
    """
    with open(f_name, "r") as f:
        return f.read(num_first_symbols)


@contextmanager
def timer():
    """
    Контекстный менеджер - замеряет время работы кода
    """  
    start = default_timer()
    yield 
    end = default_timer()
    print(f"Time: {end-start}")
    return end - start


def intro():
    """
    Первый пример: создание файла и изменения его через mmap
    """
    with temp_file("/tmp/hello.txt") as file_name:
        print(f"Before: {read_file(file_name)}")
        with open(file_name, "r+b") as f:    
            with mmap.mmap(f.fileno(), offset=0, length=0, access=mmap.ACCESS_WRITE) as mm:          
                mm[:2] = b"BB"
                print(f"Memory: {mm[:10]}")                            
        
        print(f"After: {read_file(file_name)}")


def performance():       
    """
    Сравнение производительности чтения файла в буфер обычным образом и через mmap
    """
    def perf_open(f_name: str) -> int:
        with open(f_name, "rb") as f:
            content = f.read()
            return content[:20] + content[-20:]            

    def perf_mmap(f_name: str) -> int:
        with open(f_name, "r+b") as f:
            with mmap.mmap(f.fileno(), offset=0, length=0, access=mmap.ACCESS_READ) as mm:
                return mm[:20] + mm[-20:]
                  
    with temp_file("/tmp/hello.txt", 1000_000) as file_name:
        with timer():
            perf_open(file_name)
        with timer():
            perf_mmap(file_name)        


def numpy_mapping():
    """
    Пример использования numpy
    """
    # имя файла для отображения
    f_name = 'file_for_memmap.txt'
    with temp_file("/tmp/hello.txt") as f_name:   
        # записываем туда бинарное представление массива numpy      
        with open(f_name, 'wb') as f:
            arr = np.arange(0, 100, dtype=np.int64)            
            f.write(arr.data)
            
        # отображаем файл на память
        with open(f_name, 'r+b') as f:
            with mmap.mmap(f.fileno(), length=100*8, offset=0, access=mmap.ACCESS_WRITE) as mm:
               # восстанавливаем массив
               arr = np.frombuffer(mm, dtype=np.int64)
               print(arr)  
               del arr
   

if __name__ == '__main__':
    #intro()
    # performance()    
    numpy_mapping()
