import threading
import time

lock = threading.Lock()
cond = threading.Condition(lock)

def thread_func1(name):
    print(f"{name} tentando adquirir o lock...")
    with lock:
        print(f"{name} entrou na seção crítica.")
        time.sleep(2)
    print(f"{name} liberou o lock.")

def thread_func2(name):
    print(f"{name} tentando adquirir o lock...")
    with cond:
        print(f"{name} entrou na seção crítica.")
        time.sleep(2)
    print(f"{name} liberou o lock.")

t1 = threading.Thread(target=thread_func1, args=("Thread-1",))
t2 = threading.Thread(target=thread_func2, args=("Thread-2",))

t1.start()
t2.start()
