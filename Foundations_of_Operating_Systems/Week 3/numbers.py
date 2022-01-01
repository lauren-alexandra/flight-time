import random 
from time import perf_counter

start = perf_counter() 
f = open("file2.txt", "a")

for i in range(1000000):
    rand = random.randint(0, 10000)
    f.write("% s\n" % (rand))

f.close()
print(perf_counter() - start, "seconds")