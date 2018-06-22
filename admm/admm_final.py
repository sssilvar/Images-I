import os

import numpy as np
from numpy import dot, eye
from numpy.linalg import solve

import matplotlib.pyplot as plt
plt.style.use('ggplot')

current_path = os.path.dirname(os.path.realpath(__file__))


if __name__ == '__main__':
    # Set data dimensions
    # Number of subjects: n
    # Number of structural features: dx
    # Number of non-structural features: dy
    # Number of centers: m
    # number_of_iterations: n_iter
    n = 3000
    dx_list = [10, 300, 1000, 3000]
    dy = 20
    m = 20
    n_iter = 25
    rho = 0.1

    # Set a number of experiments
    n_experiments = 15
    err = np.empty([n_experiments, n_iter])
    legends = []

    # Folders
    data_folder = os.path.join(current_path, 'data')
    global_folder = os.path.join(data_folder, 'global')

    for dx in dx_list:
        for exp_i in range(n_experiments):
            # Create data
            X = np.random.randn(n, dx) + np.random.randn(n, dx)
            W = np.random.randn(dy, dx).T
            Y = dot(X, W)

            # global_data = {'X': X, 'W': W, 'Y': Y}

            # print('[  INFO  ] Saving global matrices')
            # for key, data in global_data.items():
            #     print('\t\t- Shape of matrix %s: %s' % (key, str(data.shape)))
            #
            #     filename = os.path.join(global_folder, key + '.npy')
            #     np.save(filename, data)

            # Split data in number of centers
            print('\n\n[  INFO  ] Splitting data between %d centers' % m)
            X_split = np.split(X, m, axis=0)
            Y_split = np.split(Y, m, axis=0)

            # Start ADMM
            print('\n[  INFO  ] Starting ADMM')
            print('[  INFO  ] Initializing ~W')

            W_tilde = np.zeros([dx, dy])
            # W_tilde = np.random.normal(1, 1, [dx, dy])

            # Initialize W_k and alpha_i
            W_k = np.array([np.zeros([dx, dy])] * m)
            alpha_k = np.array([np.zeros([dx, dy])] * m)

            # W_k = np.random.normal(1,1,[dx, dy])
            # alpha_k = np.random.normal(1, 1, [dx, dy])

            for k in range(n_iter):
                for i in range(m):
                    X_i, Y_i = X_split[i], Y_split[i]
                    print('[  INFO  ] Processing center ', i, ' | Iteration : ', k)
                    print('\t\t- Shape of matrix X: ', X_split[i].shape)
                    print('\t\t- Shape of matrix Y: ', Y_split[i].shape)

                    # Update W_k
                    term_1 = solve(dot(X_i.T, X_i) + rho * eye(dx), eye(dx))  # Shape: (dx x dx)
                    term_2 = dot(X_i.T, Y_i) - alpha_k[i] + rho * W_tilde  # Shape: (dx x dy)
                    W_k[i] = dot(term_1, term_2)
                    print(W_tilde.shape)
                    print(W_k[i].shape)

                    # Update alpha_k
                    alpha_k[i] = alpha_k[i] + rho * (W_k[i] - W_tilde)
                W_tilde = np.sum(alpha_k / rho + W_k, axis=0) / m

                # Check error
                error_i = np.mean(np.abs((W - W_tilde) / W))
                print(error_i)
                err[exp_i, k] = error_i
            legends.append('Exp. ' + str(exp_i + 1))

        print('\n\n[   INFO  ] End of iterations')
        print('\t\t- Shape of matrix W:\t', W.shape)
        print('\t\t- Shape of matrix ~W:\t', W_tilde.shape)

        plt.figure(figsize=(19.2, 10.8), dpi=150)
        plt.plot(err.T)
        plt.xlabel('Number of iterations')
        plt.ylabel('Mean absolute error')
        plt.legend(legends)
        plt.title('MAE convergence (%d centers) | N = %d | dx = %d | dy = %d | rho %d' % (m, n, dx, dy, rho))

        print('[  INFO  ] Saving plot...')
        plt.savefig(os.path.join(current_path, 'data', 'admm_dx_%d_dy_%d_n_%d.png' % (dx, dy, n)), bbox_inches='tight')
        print('\t\t[  OK  ] Plot saved!')
        # plt.show()
