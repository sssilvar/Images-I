import numpy as np

import pandas as pd
import seaborn as sns
sns.set_style("white")

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


if __name__ == '__main__':
    # Load dataset
    iris = sns.load_dataset('iris')

    X = iris.drop('species', axis=1).values
    Y = iris['species'].values

    # Scale the features
    X_std = StandardScaler().fit_transform(X)
    
    # Data from "Lecture 47 — Singular Value Decomposition | Stanford University"
    # X_std = np.array([[1,3,4,5,0,0,0], [1,3,4,5,2,0,1], [1,3,4,5,0,0,0], [0,0,0,0,4,5,2], [0,0,0,0,4,5,2]]).T

    # Decompose
    U, s, VT = np.linalg.svd(X_std)
    print('\nSVD (U):\n%s' % U)
    print('\nSVD (V):\n%s' % VT)
    print('\nSVD (s):\n%s' % s[:4])

    # ############################################
    # PCA
    # ############################################
    n_comps = 3
    pca = PCA(n_components=n_comps)
    pca.fit(X_std)

    print('\nPCA components:\n%s' % pca.components_)
    print('\nVariance:\n%s' % pca.explained_variance_)
    
    result = pd.DataFrame(pca.transform(X_std), columns=['PCA%i' % i for i in range(3)])
    
    fig = plt.figure()
    
    iris['species'] = pd.Categorical(iris['species'])
    my_color = iris['species'].cat.codes

    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(result['PCA0'], result['PCA1'], result['PCA2'], c=my_color, cmap="Set2_r", s=60)

    # make simple, bare axis lines through space:
    xAxisLine = ((min(result['PCA0']), max(result['PCA0'])), (0, 0), (0,0))
    ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r')
    yAxisLine = ((0, 0), (min(result['PCA1']), max(result['PCA1'])), (0,0))
    ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r')
    zAxisLine = ((0, 0), (0,0), (min(result['PCA2']), max(result['PCA2'])))
    ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r')
    
    # label the axes
    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    ax.set_zlabel("PC3")
    ax.set_title("PCA on the iris data set")
    plt.show()


