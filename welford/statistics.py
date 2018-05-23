import numpy as np


class Statistics:
    n = 0
    mean = 0
    std = 0

    def init(self, no, mo, so):
        self.n = no
        self.mean = mo
        self.std = so

        if self.n is 0:
            print('[  WARNING  ] number of observations is 0')
            self.mean = 0
            self.std = 0

    def update_stats(self, new_data):
        # Calculate the statistics
        new_data = np.array(new_data)
        new_mean = new_data.mean()
        new_std = new_data.std()
        new_n = len(new_data)

        self.mean = np.mean([self.mean, new_mean])
        self.n = self.n + new_n
        self.std = np.sqrt(self.n * new_std - self.std ** 2) / self.n
