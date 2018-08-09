import numpy as np
from sklearn.cross_decomposition import PLSCanonical, PLSRegression, CCA

import matplotlib.pyplot as plt

plt.style.use('ggplot')


if __name__ == '__main__':
    # #############################################################################
    # PLS regression, with multivariate response, a.k.a. PLS2

    n = 1000
    q = 3
    p = 10
    np.random.seed(42)

    X = np.random.normal(size=n * p).reshape((n, p))
    B = np.array([[1, 2] + [0] * (p - 2)] * q).T
    # each Yj = 1*X1 + 2*X2 + noize
    Y = np.dot(X, B) + np.random.normal(size=n * q).reshape((n, q)) + 5

    pls2 = PLSRegression(n_components=3)
    pls2.fit(X, Y)
    print("True B (such that: Y = XB + Err)")
    print(B)
    
    # compare pls2.coef_ with B
    print("Estimated B")
    print(np.round(pls2.coef_, 1))
    pls2.predict(X)

    # PLS regression, with univariate response, a.k.a. PLS1
    n = 1000
    p = 10

    X = np.random.normal(size=n * p).reshape((n, p))
    y = X[:, 0] + 2 * X[:, 1] + np.random.normal(size=n * 1) + 5

    pls1 = PLSRegression(n_components=3)
    pls1.fit(X, y)
    
    # note that the number of components exceeds 1 (the dimension of y)
    print("Estimated betas")
    print(np.round(pls1.coef_, 1))