# Split file1.txt into 2 parts and read each part into memory separately.

import random 
from time import perf_counter

start = perf_counter() 
new_file_4 = open("new_file_4.txt", "w+")
num_file_pt1 = open('file1copy_00.txt', 'r')
num_file_pt2 = open('file1copy_01.txt', 'r')

f1 = num_file_pt1.read()
f2 = num_file_pt2.read()

f1 = f1.split('\n')
f2 = f2.split('\n')

for num in f1:
    if (num != ''):
        num = num.strip()
        doubled = int(num) * 2
        new_file_4.write("% s\n" % (doubled))

for num in f2:
    if (num != ''):
        num = num.strip()
        doubled = int(num) * 2
        new_file_4.write("% s\n" % (doubled))

new_file_4.close() 
print(perf_counter() - start, "seconds")