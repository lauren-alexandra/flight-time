import threading
import random
from time import perf_counter

f = open("file4.txt", "a") 

def write_rand(lock):
    for i in range(250000):
        lock.acquire()
        rand = random.randint(0, 10000)
        f.write("% s\n" % (rand))
        lock.release()

# creating a lock
lock = threading.Lock()

# creating threads
t1 = threading.Thread(target=write_rand, args=(lock,))
t2 = threading.Thread(target=write_rand, args=(lock,))
t3 = threading.Thread(target=write_rand, args=(lock,))
t4 = threading.Thread(target=write_rand, args=(lock,))

start = perf_counter() 

# starting threads
t1.start()
t2.start()
t3.start()
t4.start()

# wait until all threads have completely executed
t1.join()
t2.join()
t3.join()
t4.join()

# threads completely executed
print(perf_counter() - start, "seconds")
f.close()