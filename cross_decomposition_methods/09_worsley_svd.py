import os

import numpy as np
from numpy.linalg import eig, inv, svd

from scipy.spatial import distance

import matplotlib.pyplot as plt


# Initial setup
np.set_printoptions(precision=3, suppress=True)
os.system('clear')
plt.style.use('ggplot')

# Create data
np.random.seed(42)
n = 500
dx = 20
dy = 5000

X = np.random.normal(size=[n, dx])
W = np.random.normal(size=[dx, dy])
Y = X.dot(W) + np.random.normal(size=[n, dy])

plt.scatter(X.dot(W)[0], Y[0])
# plt.show()

X, Y = X.T, Y.T
# Calculate cross-covariance matrix as X'Y: cxy
cxy = X.dot(Y.T)
print('S = X\'Y (shape): %s' % str(cxy.shape))

# Calculate cross-covariance matrix as XX'YY': cxxyy
cxxyy = X.T.dot(X).dot(Y.T).dot(Y)
print('S = XX\'YY\' (shape): %s' % str(cxxyy.shape))

# #####################################################
# SVD (PLS-SVD)
# #####################################################
U, s, VT = svd(cxy)
S = np.diag(s)

# #####################################################
# SVD (PLS-SVD) - Worsley
# #####################################################
# Get eigen vectors (X'XY'Y)A=AL
L, A = eig(cxxyy)

# Calculate B=A(A'Y'YA)^(1/2)
term = 1 / np.sqrt(np.abs(A.T.dot(Y.T).dot(Y).dot(A)))
B = A.dot(term)

# Calculate singular values: W
W = np.sqrt(np.diag(L))

# Calculate proyection matrices:
# U = X(Y'YBW^-1)
# v = YB
U = X.dot(Y.T.dot(Y).dot(B).dot(inv(W)))
V = Y.dot(B)

print(np.diag(S))
print(np.diag(np.real(W)))

