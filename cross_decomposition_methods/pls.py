import numpy as np
import pandas as pd
from sklearn import datasets

import matplotlib.pyplot as plt

plt.style.use('ggplot')


if __name__ == '__main__':
    # Load dataset
    iris = datasets.load_iris()
    df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])
    print(df.head())

    # Plot Lenghts
    fig, ax = plt.subplots()    
    cax = ax.scatter(df['sepal length (cm)'], df['petal length (cm)'], c=df['target'], cmap='viridis')
    
    cbar = fig.colorbar(cax, ticks=[0, 1, 2], orientation='vertical')
    cbar.ax.set_yticklabels(iris.target_names)  # horizontal colorbar

    # plt.show()

    # Do PLS
    X = np.array(df['sepal length (cm)'])
    Y = np.array(df['petal length (cm)'])

    # A. Initialize u
    u = np.array(Y[0])
    err = 10

    while err > 1e-4:
        # B. X-weights
        w = X.T.dot(u) / (u.T.dot(u))

        # C. Calculate the X-scores
        t = np.array(X.dot(w))

        # D. Calculate Y-weigths
        c = Y.T / t.T.dot(t)

        # E. Update Y-scores
        u = Y.dot(c) / c.T.dot(c)

        
        t_old = t.copy()

    
