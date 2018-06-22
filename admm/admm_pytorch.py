import os


import torch

import matplotlib.pyplot as plt
plt.switch_backend('agg')
plt.style.use('ggplot')

current_path = os.path.dirname(os.path.realpath(__file__))

# dtype=torch.cuda.FloatTensor
dtype = torch.FloatTensor

if __name__ == '__main__':
    # Set data dimensions
    # Number of subjects: n
    # Number of structural features: dx
    # Number of non-structural features: dy
    # Number of centers: m
    # number_of_iterations: n_iter
    dx_list = [10] #, 1000, 3000]  #, 10000]
    dy = 20000
    m = 10
    n_iter = 100
    rho = 0.01

    # Set a number of experiments
    n_experiments = 15
    err = torch.empty([n_experiments, n_iter])
    legends = []

    # generate ticks for xlabel
    x_ticks = range(1, n_iter + 1)

    # Folders
    data_folder = os.path.join(current_path, 'data')
    global_folder = os.path.join(data_folder, 'global')

    for dx in dx_list:
        # n = int(dx * 0.8)
        n = 3000
        # Set subject of observations based on the number of features
        for exp_i in range(n_experiments):
            # Create data
            X = torch.randn(n, dx).type(dtype)
            W = torch.randn(dy, dx).t().type(dtype)
            Y = (torch.mm(X, W) + 0.1 * torch.randn(n, dy)).type(dtype)

            # W_full_data  = torch.solve(torch.mm(X.t(),X), torch.mm(X.t(),Y))

            global_data = {'X': X, 'W': W, 'Y': Y}

            print('[  INFO  ] Saving global matrices')
            for key, data in global_data.items():
                print('\t\t- Shape of matrix %s: %s' % (key, str(data.shape)))

                # filename = os.path.join(global_folder, key + '.npy')
                # np.save(filename, data)
            print('\t\t- Number of observations: ', n)

            # Split data in number of centers
            print('\n\n[  INFO  ] Splitting data between %d centers' % m)
            X_split = torch.chunk(X, m, dim=0)
            Y_split = torch.chunk(Y, m, dim=0)

            # Start ADMM
            print('\n[  INFO  ] Starting ADMM')
            print('[  INFO  ] Initializing ~W')

            W_tilde = torch.zeros([dx, dy]).type(dtype)
            # W_tilde = np.random.normal(1, 1, [dx, dy])

            # Initialize W_k and alpha_i
            W_k = torch.stack([torch.zeros([dx, dy]).type(dtype)] * m)
            alpha_k = torch.stack([torch.zeros([dx, dy]).type(dtype)] * m)

            # W_k = np.random.normal(1,1,[dx, dy])
            # alpha_k = np.random.normal(1, 1, [dx, dy])

            for k in range(n_iter):
                for i in range(m):
                    X_i, Y_i = X_split[i].type(dtype), Y_split[i].type(dtype)
                    print('[  INFO  ] Processing center ', i, ' | Iteration : ', k, ' Experiment ', exp_i + 1)
                    # print('\t\t- Shape of matrix X: ', X_split[i].shape)
                    # print('\t\t- Shape of matrix Y: ', Y_split[i].shape)
                    # print('\t\t- Shape of matrix W: ', W_k.shape)

                    # Update W_k
                    term_1 = torch.inverse(torch.mm(X_i.t(), X_i) + rho * torch.eye(dx).type(dtype))  # Shape: (dx x dx)
                    term_2 = torch.mm(X_i.t(), Y_i) - alpha_k[i] + rho * W_tilde  # Shape: (dx x dy)
                    W_k[i] = torch.mm(term_1, term_2)
                    print(W_tilde.shape)
                    print(W_k[i].shape)

                    # Update alpha_k
                    alpha_k[i] = alpha_k[i] + rho * (W_k[i] - W_tilde)
                W_tilde = torch.sum(alpha_k / rho + W_k, dim=0) / m

                # Check error
                error_i = torch.mean(torch.abs((W - W_tilde)**2)).type(torch.FloatTensor)
                print('\t\t- Error: ', error_i.numpy())
                err[exp_i, k] = error_i
            legends.append('Exp. ' + str(exp_i + 1))

        print('\n\n[   INFO  ] End of iterations')
        print('\t\t- Shape of matrix W:\t', W.shape)
        print('\t\t- Shape of matrix ~W:\t', W_tilde.shape)

        plt.figure(figsize=(19.2, 10.8), dpi=150)
        plt.plot(err.numpy().T)
        plt.xlabel('Number of iterations')
        plt.ylabel('Mean square error')
        plt.legend(legends)
        plt.xticks(range(n_iter), x_ticks)
        plt.title('MSE convergence (%d centers) | N = %d | dx = %d | dy = %d | rho %.2f' % (m, n, dx, dy, rho))

        print('[  INFO  ] Saving plot...')
        plt.savefig(os.path.join(current_path, 'data', 'admm_dx_%d_dy_%d_n_%d.png' % (dx, dy, n)), bbox_inches='tight')
        print('\t\t[  OK  ] Plot saved!')
        # plt.show()
