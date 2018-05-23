import numpy as np
from welford import Welford

if __name__ == '__main__':
    data = []
    stats = []
    np.random.seed(10)
    for i in range(1, 11):
        buffer = np.random.normal(i, i/2, 2000)
        data.append(buffer)
        stats.append(Welford())
        print('Column %d | mean: %f | std: %f' % (i, buffer.mean(), buffer.std()))

    # Real data vector: 300 files (observations), 10 columns (features)
    data = np.array(data).T

    data_split = np.split(data, 100)
    print('\n\n\t RESULTS: \n')

    # for i, row in enumerate(data.T):
    #     print('Column %d | mean: %f' % (i + 1, row.mean()))

    for i, sub_data in enumerate(data_split):
        for j, col in enumerate(sub_data.T):
            if i == 0:
                stats[j].k = 1
                stats[j].M = np.mean(col)
                stats[j].S = np.std(col)
            else:
                stats[j](col)

    for i, stat in enumerate(stats):
        print('Column %d | mean: %f | std: %f' % (i, stat.mean, stat.std))



