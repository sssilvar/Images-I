import os
import numpy as np
from multiprocessing import Pool

array = np.random.normal(loc=0, scale=1, size=100)
pwd = os.path.dirname(os.path.realpath(__file__))


def pr(t):
    for i in range(len(array)):
        # os.system('echo "Hello %d"' % i)
        os.system('bash %s' % os.path.join(pwd, 'usage.sh'))


pool = Pool()
pool.map(pr, array)
pool.close()
pool.join()
