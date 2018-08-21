import os
import time

import numpy as np
from numpy.linalg import eig, inv, norm, svd

from scipy.spatial import distance

import matplotlib.pyplot as plt


# Initial setup
np.set_printoptions(precision=3, suppress=True)
os.system('clear')
plt.style.use('ggplot')

# Create data
np.random.seed(42)
n = 100
dx = 20
dy = 1500

X = np.random.normal(size=[n, dx])
W = np.random.normal(size=[dx, dy])
Y = X.dot(W) + np.random.normal(size=[n, dy])

# plt.scatter(X.dot(W)[0], Y[0])
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
U_xy, s_xy, VT_xy = svd(cxy)
V_xy = VT_xy.T

# #####################################################
# SVD (PLS-SVD) - Lorenzi, silva
# #####################################################
from plsr import PLSR

ti = time.time()

plsr = PLSR(X.T, Y.T)
plsr.calculate_covariances()
plsr.evaluate()
U_s, V_s = plsr.scores()
cx, cy = plsr.components()

tf = time.time()
t_si = tf - ti

# #####################################################
# SVD (PLS-SVD) - Worsley
# #####################################################
ti = time.time()
# Get eigen vectors (X'XY'Y)A=AL
L, A = eig(cxxyy)

# Calculate B=A(A'Y'YA)^(1/2)
S = np.diag(A.T.dot(Y.T).dot(Y).dot(A))
term = 1 / np.sqrt(S)
B = A.dot(np.diag(term))

# Calculate singular values: W
W = np.sqrt(np.diag(L))

# Calculate proyection matrices:
# U = X(Y'YBW^-1)
# v = YB
U_xxyy = np.real(X.dot(Y.T.dot(Y).dot(B).dot(inv(W))))
V_xxyy = np.real(Y.dot(B))
tf = time.time()
t_wo = tf - ti

# #####################################################
# SVD (PLS-SVD) - Lorenzi
# #####################################################
from PLSR import PLSR

ti = time.time()

plsr = PLSR(X.T, Y.T)
plsr.Initialize()
plsr.EvaluateComponents()
U_lz, V_lz = plsr.GetWeights()
Cx, Cy = plsr.ReturnComponents()

tf = time.time()
t_lo = tf - ti

print('PLS-SVD:\n%s' % U_xy[:3,:8])
print('Worsley:\n%s' % U_xxyy[:3,:8])
print('Lorenzi:\n%s' % U_lz[:3,:])
print('Silva:\n%s' % U_s[:3,:])

print('Execution times:\n- %f\n- %f\n- %f' % (t_wo, t_lo, t_si))

# print(cx[:3,:])
# print(Cx[:3,:])


