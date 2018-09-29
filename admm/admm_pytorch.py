import os

import torch
import pandas as pd

import matplotlib.pyplot as plt

plt.switch_backend('agg')
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 36})

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
    n = 2400
    n_iter = 10
    n_sub_exp = 5
    m = n_sub_exp * 5
    torch.manual_seed(42)

    # Set a number of experiments
    n_experiments = n_sub_exp * 4
    n_centers = [10, 40, 60, 100]

    rho_vec = [1e-2, 10, 100, 1000]

    # Set error vector
    err = torch.empty([n_experiments, n_iter])
    legends = []
    dfs = []

    # Folders
    data_folder = os.path.join(current_path, 'data')
    global_folder = os.path.join(data_folder, 'global')

    for dx in dx_list:
        # Set subject of observations based on the number of features
        for exp_i in range(n_experiments):
            # Set rho
            # rho = rho_vec[exp_i]
            rho = 0.001
            m = n_centers[exp_i // n_sub_exp]

            # Create data
            X = torch.randn(n, dx).type(dtype)
            W = torch.randn(dy, dx).t().type(dtype)
            Y = torch.mm(X, W).type(dtype) + 2 * torch.randn(n, dy).type(dtype)

            X_t_X, LU = torch.gesv(torch.eye(dx).type(dtype), torch.mm(X.t(), X))
            W_full_data = torch.mm(X_t_X, torch.mm(X.t(), Y))
            
            # print('Plotting')
            # plt.scatter(Y.numpy()[0], torch.mm(X, W).numpy()[0], alpha=0.2, color='b')
            # plt.show() 

            global_data = {'X': X, 'W': W, 'Y': Y}

            # Print info
            print('\n[  INFO  ] ==== Experiment %d ====' % exp_i)
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
                error_i = torch.mean(torch.abs((W - W_tilde) ** 2)).type(torch.FloatTensor)
                # error_i = torch.norm(W - W_tilde).type(torch.FloatTensor)
                print('\t\t- Error: ', error_i.numpy())
                err[exp_i, k] = error_i

                for i in range(m):
                    X_i, Y_i = X_split[i].type(dtype), Y_split[i].type(dtype)
                    # print('[  INFO  ] Processing center ', i, ' | Iteration : ', k, ' Experiment ', exp_i + 1)

                    # Update W_k
                    term_1, _ = torch.gesv(torch.eye(dx).type(dtype), torch.mm(X_i.t(), X_i) + 0.5 * rho * torch.eye(dx).type(dtype))  # Shape: (dx x dx)
                    term_2 = torch.mm(X_i.t(), Y_i) - 0.5 * alpha_k[i] + 0.5 * rho * W_tilde  # Shape: (dx x dy)
                    W_k[i] = torch.mm(term_1, term_2)
                    # print(W_tilde.shape)
                    # print(W_k[i].shape)

                    # Update alpha_k
                    alpha_k[i] = alpha_k[i] + rho * (W_k[i] - W_tilde)
                W_tilde = torch.sum(alpha_k / rho + W_k, dim=0) / m

            # legends.append('Rho = %.1E' % rho)
            # legends.append('%d centers' % m)
            if exp_i in [i + (n_sub_exp - 1) for i in range(0, n_experiments + 1, n_sub_exp)]:
                df_i = pd.DataFrame(err.numpy()[exp_i - n_sub_exp + 1:exp_i + 1, :])
                dfs.append(df_i)
                legends.append('%d centers' % m)
                print(df_i.shape)
                print(df_i.std())

        print('\n\n[   INFO  ] End of iterations')
        print('\t\t- Shape of matrix W:\t', W.shape)
        print('\t\t- Shape of matrix ~W:\t', W_tilde.shape)

        # plt.figure(figsize=(19.2 * 0.7, 10.8 * 0.7), dpi=150)
        fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(9*4, 9))
        for df in dfs:
            ax0.fill_between([i for i in range(n_iter)], df.mean() - df.std(), df.mean() + df.std(), alpha=0.6)
            ax0.plot(df.mean())
        ax0.set_xlabel('Number of iterations')
        ax0.set_ylabel('$MSE(\mathbf{W}, \widetilde{\mathbf{W}})$')
        ax0.legend(legends)
        ax0.margins(0.05, 0.07)
        ax0.set_yscale('log')
        ax0.grid(b=True, which='minor', linestyle='-', alpha=0.2)
        # plt.title('MSE convergence (%d centers) | N = %d | dx = %d | dy = %d' % (m, n, dx, dy))

        X, Y = X.to('cpu'), Y.to('cpu')
        W, W_tilde = W.to('cpu'), W_tilde.to('cpu')
        
        # Subplot 2: W vs W_tilde
        ax1.scatter(W.numpy()[0], W_tilde.numpy()[0], color='#011627', edgecolors='w')
        ax1.set_xlabel('$\mathbf{w}$')
        ax1.set_ylabel('$\widetilde{\mathbf{w}}$ (estimated)')

        # plt.subplot(222)
        # plt.scatter(Y.numpy()[0], torch.mm(X, W).numpy()[0], alpha=0.3, color='b', edgecolors='w')
        
        # plt.subplot(224)
        # plt.scatter(Y.numpy()[0], torch.mm(X, W_tilde).numpy()[0], alpha=0.3, color='r')


        print('[  INFO  ] Saving plot...')
        out_file = os.path.join(current_path, 'data', 'admm_dx_%d_dy_%d_n_%d' % (dx, dy, n))
        plt.savefig(out_file + '.png', bbox_inches='tight')
        plt.savefig(out_file + '.pdf', bbox_inches='tight')
        print('\t\t[  OK  ] Plot saved!')
        # plt.show()
