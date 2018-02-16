import os
import numpy as np
from multiprocessing import Pool

array = np.random.normal(loc=0, scale=1, size=10000)


def pr(t):
    for i in range(10000):
        os.system('echo "Hello %d"' % i)


pool = Pool()
pool.map(pr, array)
pool.close()
pool.join()
