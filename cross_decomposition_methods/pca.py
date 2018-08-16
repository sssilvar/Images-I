import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import matplotlib.pyplot as plt
plt.style.use('ggplot')

if __name__ == '__main__':
    # Load dataset
    iris = sns.load_dataset('iris')

    X = iris.drop('species', axis=1).values
    Y = iris['species'].values

    # Scale the features
    X_std = StandardScaler().fit_transform(X)

    # Calculate the correlation matrix in the features
    cov_matrix = np.cov(X_std.T)
    print('\nCovariance Matrix:\n%s' % cov_matrix)
    
    plt.figure()
    plt.imshow(cov_matrix, cmap='jet')
    plt.grid('off')
    plt.title('Covariance matrix of features')
    plt.xticks([0, 1, 2, 3], iris.columns[:-1], rotation='vertical')
    plt.yticks([0, 1, 2, 3], iris.columns[:-1])
    plt.colorbar()

    # Get the eigen vectors
    eig_vals, eig_vecs = np.linalg.eig(cov_matrix)
    print('\nEigenvectors:\n%s' % eig_vecs)
    print('\nEigenvalues:\n%s' % eig_vals)

    # Check who containes the greatest variances
    comps = [comp / eig_vals.sum() for comp in eig_vals]
    print('\nPercentage of variance:\n%s' % comps)
    # As the first contains almost 73% we select 1 dimension

    # Project the data onto selected eigen vector
    proj_X = np.array([X_std.dot(eig_vecs.T[0]), X_std.dot(eig_vecs.T[1])]).T

    # Save it into a DataFrame
    result = pd.DataFrame(proj_X, columns=['PC1', 'PC2'])
    result['y-axis'] = 0
    result['label'] = Y

    print(result.head())

    # ############################################
    # DONE WITH PCA LIBRARY
    # ############################################
    pca = PCA(n_components=1)
    pca_x = pca.fit_transform(X_std)

    print(pca.explained_variance_)

    sk_result = pd.DataFrame(pca_x, columns=['PC1'])
    sk_result['y-axis'] = 0
    sk_result['label'] = Y


    # Plot results
    sns.lmplot('PC1', 'y-axis', data=result, fit_reg=False,
                scatter_kws={'s': 50},  # Marker size
                hue='label')  # Color
    plt.title('PCA Result')

    # Plot results
    sns.lmplot('PC1', 'y-axis', data=sk_result, fit_reg=False,
                scatter_kws={'s': 50},  # Marker size
                hue='label')  # Color
    plt.title('PCA Result (Skleran)')

    
    # Show Plots
    # plt.show()