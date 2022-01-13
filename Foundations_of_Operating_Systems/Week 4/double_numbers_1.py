# Read the entire contents of file1.txt into memory, then process each row.

import random 
from time import perf_counter

start = perf_counter() 
new_file_2 = open("new_file_2.txt", "w+")
num_file = open('file1.txt', 'r')
# Read the entire contents of file1.txt into memory. 
# The read() function is designed to be called once, and it returns the entire contents of the file. 
f = num_file.read()

# then process each row 
f = f.split('\n')
for num in f:
    if (num != ''):
        num = num.strip()
        doubled = int(num) * 2
        new_file_2.write("% s\n" % (doubled))

new_file_2.close() 
print(perf_counter() - start, "seconds")