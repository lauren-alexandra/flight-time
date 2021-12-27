import random 

f = open("file2.txt", "a")

for i in range(1000):
    rand = random.randint(0, 10000)
    f.write("% s\n" % (rand))

f.close()