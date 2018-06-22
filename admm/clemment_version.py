import numpy as np


def generate_data(n, dx, dy):
    X = np.random.randn(n, dx)
    W = np.random.randn(dy, dx)
    Y = np.dot(X, W.T)

    return Y, X, W


def closed_form_solution(X, Y):
    return np.dot(np.linalg.inv(np.dot(X.T, X)), np.dot(X.T, Y)).T


def update(W_tilde, Xi, Yi, rho):
    term1 = np.dot(Xi.T,Xi) + rho * np.eye(Xi.shape[1])
    term1_inv = np.linalg.solve(term1, np.eye(term1.shape[0]))
    term2 = np.dot(Xi.T,Yi) + rho * W_tilde.T
    res = np.dot(term1_inv, term2)

    return res.T


def cost_i(W_tilde, Wi, Xi, Yi, rho):
    term1 = np.sum((Yi - np.dot(Xi,Wi.T))**2)
    term2 = rho * np.sum((Wi - W_tilde) ** 2)
    return term1 + term2


def optim_l2_constraint(X, Y, W_sol, n, dx, dy, rho, n_batch):
    eps = 10e-5
    max_iter = 1000
    split = n // n_batch

    W_i = np.random.randn(n_batch, dy, dx)
    W_tilde = np.random.randn(dy, dx)

    costs = []
    lims = []
    for i in range(max_iter):
        cost = np.sum([cost_i(W_tilde, W_i[p], X[p*split:(p+1)*split, :], Y[p*split:(p+1)*split, :], rho)
                       for p in range(n_batch)])
        costs.append(cost)
        # print('Cost = ' + str(cost))
        lim = np.sum(np.abs(W_tilde - W_sol))
        lims.append(lim)
        # print('lim = ' + str(lim))

        if lim < eps:
            # print('Sol has converged')
            break

        for j in range(n_batch):
            W_i[j] = update(W_tilde, X[j*split:(j+1)*split,:], Y[j*split:(j+1)*split,:], rho)

        W_tilde = np.sum(W_i, axis=0) / n_batch

    return costs, lims, W_tilde


if __name__=='__main__':
    n = 10000
    dx = 50
    dy = 20
    rho = 0.001
    n_batch = 100

    Y, X, W = generate_data(n, dx, dy)
    W_sol = closed_form_solution(X, Y)
    costs, lims, W_tilde = optim_l2_constraint(X, Y, W_sol, n, dx, dy, rho, n_batch)
    assert len(lims) == len(costs)
    print(np.mean(np.abs((W - W_tilde) / W)))
    print('Sol converged in {} steps'.format(len(lims)))
