from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from time import perf_counter

start = perf_counter() 

totalfile = open("totalfile_method2.txt", "w+") 

def job(file1, file2):
    file_1 = f"C:\\Users\\laure_ou\\Documents\\Projects\\CSC507\\PortfolioMilestone8\\{file1}.txt"
    file_2 = f"C:\\Users\\laure_ou\\Documents\\Projects\\CSC507\\PortfolioMilestone8\\{file2}.txt"
    huge_file_1 = open(file_1, 'r')
    huge_file_2 = open(file_2, 'r')
    num_file_1 = huge_file_1.read()
    num_file_2 = huge_file_2.read()
    f1 = num_file_1.split('\n')
    f2 = num_file_2.split('\n')

    for i in len(f1.readlines()):
        num1 = f1[i].strip()
        num2 = f2[i].strip()
        if (num1 != "" and num2 != ""):
            sum = int(num1) + int(num2)
            totalfile.write("% s\n" % (sum))

def multiprocessing(func, args, workers):
    with ProcessPoolExecutor(workers) as ex:
        res = ex.map(func, args)
    return list(res)

set1 = ['small_file_1.txt', 'small_file_11.txt']
set2 = ['small_file_2.txt', 'small_file_12.txt']
set3 = ['small_file_3.txt', 'small_file_13.txt']
set4 = ['small_file_4.txt', 'small_file_14.txt']
set5 = ['small_file_5.txt', 'small_file_15.txt']
set6 = ['small_file_6.txt', 'small_file_16.txt']
set7 = ['small_file_7.txt', 'small_file_17.txt']
set8 = ['small_file_8.txt', 'small_file_18.txt']
set9 = ['small_file_9.txt', 'small_file_19.txt']
set10 = ['small_file_10.txt', 'small_file_20.txt']

n_jobs = 4
start = perf_counter() 
# run process on all 10 sets in parallel
# 4 heavy cpu jobs, on 4 threads on a 4-cores machine 
multiprocessing(job(set1[0], set1[1]), range(n_jobs), 4)
multiprocessing(job(set2[0], set2[1]), range(n_jobs), 4)
multiprocessing(job(set3[0], set3[1]), range(n_jobs), 4)
multiprocessing(job(set4[0], set4[1]), range(n_jobs), 4)
multiprocessing(job(set5[0], set5[1]), range(n_jobs), 4)
multiprocessing(job(set6[0], set6[1]), range(n_jobs), 4)
multiprocessing(job(set7[0], set7[1]), range(n_jobs), 4)
multiprocessing(job(set8[0], set8[1]), range(n_jobs), 4)
multiprocessing(job(set9[0], set9[1]), range(n_jobs), 4)
multiprocessing(job(set10[0], set10[1]), range(n_jobs), 4)

print(perf_counter() - start, "seconds")
