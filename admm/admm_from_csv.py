import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

# plt.switch_backend('agg')
plt.style.use('ggplot')

current_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    X = pd.read_csv(
        '/disk/Data/data_simulation/all_in_one/output/common_data.csv',
        index_col=0).values
    Y = pd.read_csv(
        '/disk/Data/data_simulation/all_in_one/output/groupfile_features.csv',
        index_col=0).values

    print('Data info: \n\t- X shape %s\n\t- Y shape: %s' % (str(X.shape), str(Y.shape)))
    
    m = 3
    rho = 0.001
    n_iter = 10
    n, dx, dy = X.shape[0], X.shape[1], Y.shape[1]

    W_full_data = np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, Y))

    # START ADMM
    err = []
    W_tilde = np.zeros([dx, dy])

    W_k = [np.zeros([dx, dy])] * m
    alpha_k = [np.zeros([dx, dy])] * m

    for k in range(n_iter):
        # Check error
        error_i = np.mean(np.abs((W_full_data - W_tilde) ** 2))
        print('\t\t- Error: ', error_i)
        err.append(error_i)

        for i in range(m):
            X_i = pd.read_csv('/disk/Data/data_simulation/center_%d/output/common_data.csv' % (i+1), index_col=0).values
            Y_i = pd.read_csv('/disk/Data/data_simulation/center_%d/output/groupfile_features.csv' % (i+1), index_col=0).values
            print('Data info: \n\t- X shape %s\n\t- Y shape: %s' % (str(X_i.shape), str(Y_i.shape)))
            print('[  INFO  ] Processing center ', i, ' | Iteration : ', k)

            # Update W_k
            term_1 = np.linalg.solve(np.dot(X_i.T, X_i) + 0.5 * rho * np.eye(dx), np.eye(dx))  # Shape: (dx x dx)
            term_2 = np.dot(X_i.T, Y_i) - 0.5 * alpha_k[i] + 0.5 * rho * W_tilde  # Shape: (dx x dy)
            W_k[i] = np.dot(term_1, term_2)
            # print(W_tilde.shape)
            # print(W_k[i].shape)

            # Update alpha_k
            alpha_k[i] = alpha_k[i] + rho * (W_k[i] - W_tilde)
            print(
                'Data INFO: \n\t- Mean: %f\n\t- Std: %f'
                % (np.mean(alpha_k[i]), np.std(alpha_k[i]))
            )
        W_tilde = np.sum(np.array(alpha_k) / rho + np.array(W_k), axis=0) / m
        print('W_tilde INFO: \n\t- Mean: %f\n\t- Std: %f' % (np.mean(W_tilde), np.std(W_tilde)))
    
    # Plot results
    plt.figure(figsize=(19.2 * 0.5, 10.8 * 0.5), dpi=150)
    plt.plot(err)
    plt.xlabel('Number of iterations')
    plt.ylabel('Mean square error')
    plt.show()
