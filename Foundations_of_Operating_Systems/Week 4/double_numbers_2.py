# Read one row of file1.txt at a time and process it.

# readline()

import random 
from time import perf_counter

start = perf_counter() 
new_file_3 = open("new_file_3.txt", "w+")
num_file = open('file1.txt', 'r')

while True:
    # Get next line from file
    num = num_file.readline()

    if (num != ''):
        num = num.strip()
        doubled = int(num) * 2
        new_file_3.write("% s\n" % (doubled))
    else:
        break
 
new_file_3.close()

print(perf_counter() - start, "seconds")