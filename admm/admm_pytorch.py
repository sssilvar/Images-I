import os

import torch
import numpy as np

import matplotlib.pyplot as plt

plt.switch_backend('agg')
plt.style.use('ggplot')

current_path = os.path.dirname(os.path.realpath(__file__))

dtype=torch.cuda.FloatTensor
# dtype = torch.FloatTensor

if __name__ == '__main__':
    # Set data dimensions
    # Number of subjects: n
    # Number of structural features: dy
    # Number of non-structural features: dx
    # Number of centers: m
    # number_of_iterations: n_iter
    dy = 50000
    dx_list = [20]  # , 1000, 3000]  #, 10000]
    n = 3000
    m = 300
    n_iter = 10

    # Set a number of experiments
    n_experiments = 4
    rho_vec = [1e-2, 10, 1000, 3000]

    # Set error vector
    err = torch.empty([n_experiments, n_iter])
    legends = []

    # Folders
    data_folder = os.path.join(current_path, 'data')
    global_folder = os.path.join(data_folder, 'global')

    for dx in dx_list:
        # Set subject of observations based on the number of features
        for exp_i in range(n_experiments):
            # Set rho
            rho = rho_vec[exp_i]

            # Create data
            torch.manual_seed(42)
            X = torch.randn(n, dx).type(dtype)
            W = torch.randn(dy, dx).t().type(dtype)
            Y = torch.mm(X, W).type(dtype) + 10 * torch.randn(n, dy).type(dtype)

            X_t_X, LU = torch.gesv(torch.eye(dx).type(dtype), torch.mm(X.t(), X))
            W_full_data = torch.mm(X_t_X, torch.mm(X.t(), Y))

            global_data = {'X': X, 'W': W, 'Y': Y}

            # Print info
            print('[  INFO  ] Global matrices info:')
            for key, data in global_data.items():
                print('\t\t- Shape of matrix %s: %s' % (key, str(data.shape)))
            print('\t\t- Number of observations: ', n)

            # Split data in number of centers
            print('\n\n[  INFO  ] Splitting data between %d centers' % m)
            X_split = torch.chunk(X, m, dim=0)
            Y_split = torch.chunk(Y, m, dim=0)

            # Start ADMM
            print('\n[  INFO  ] Starting ADMM')
            print('[  INFO  ] Initializing ~W')
            print('[  INFO  ] Rho: ', rho_vec)

            W_tilde = torch.zeros([dx, dy]).type(dtype)
            # W_tilde = np.random.normal(1, 1, [dx, dy])

            # Initialize W_k and alpha_i
            W_k = torch.stack([torch.zeros([dx, dy]).type(dtype)] * m)
            alpha_k = torch.stack([torch.zeros([dx, dy]).type(dtype)] * m)

            # W_k = np.random.normal(1,1,[dx, dy])
            # alpha_k = np.random.normal(1, 1, [dx, dy])

            for k in range(n_iter):
                # Check error
                error_i = torch.mean(torch.abs((W_full_data - W_tilde) ** 2)).type(torch.FloatTensor)
                print('\t\t- Error: ', error_i.numpy())
                err[exp_i, k] = error_i

                for i in range(m):
                    X_i, Y_i = X_split[i].type(dtype), Y_split[i].type(dtype)
                    print('[  INFO  ] Processing center ', i, ' | Iteration : ', k, ' Experiment ', exp_i + 1)

                    # Update W_k
                    term_1, _ = torch.gesv(torch.eye(dx).type(dtype), torch.mm(X_i.t(), X_i) + 0.5 * rho * torch.eye(dx).type(dtype))  # Shape: (dx x dx)
                    term_2 = torch.mm(X_i.t(), Y_i) - 0.5 * alpha_k[i] + 0.5 * rho * W_tilde  # Shape: (dx x dy)
                    W_k[i] = torch.mm(term_1, term_2)
                    print(W_tilde.shape)
                    print(W_k[i].shape)

                    # Update alpha_k
                    alpha_k[i] = alpha_k[i] + rho * (W_k[i] - W_tilde)
                W_tilde = torch.sum(alpha_k / rho + W_k, dim=0) / m

            legends.append('Rho = %.1E' % rho)

        print('\n\n[   INFO  ] End of iterations')
        print('\t\t- Shape of matrix W:\t', W.shape)
        print('\t\t- Shape of matrix ~W:\t', W_tilde.shape)

        plt.figure(figsize=(19.2 * 0.5, 10.8 * 0.5), dpi=150)
        plt.plot(err.numpy().T)
        plt.xlabel('Number of iterations')
        plt.ylabel('Mean square error')
        plt.legend(legends)
        plt.margins(0.05, 0.07)
        plt.title('MSE convergence (%d centers) | N = %d | dx = %d | dy = %d' % (m, n, dx, dy))

        print('[  INFO  ] Saving plot...')
        plt.savefig(os.path.join(current_path, 'data', 'admm_dx_%d_dy_%d_n_%d.pdf' % (dx, dy, n)), bbox_inches='tight')
        print('\t\t[  OK  ] Plot saved!')
        # plt.show()
