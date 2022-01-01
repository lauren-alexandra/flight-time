import threading
import random
from time import perf_counter

f = open("file3.txt", "a") 

def write_rand(iteration):
    for i in range(iteration):
        rand = random.randint(0, 10000)
        f.write("% s\n" % (rand))
  
# creating threads
t1 = threading.Thread(target=write_rand, args=(250000,))
t2 = threading.Thread(target=write_rand, args=(250000,))
t3 = threading.Thread(target=write_rand, args=(250000,))
t4 = threading.Thread(target=write_rand, args=(250000,))

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