__author__ = "Marco Lorenzi, Santiago Silva"
__credits__ = ["Worsley et. al (2005)"]
__description__ = """A low dimensional PLSR analysis base on (Worsley et. al)."""

import numpy as np
from numpy.linalg import eig, inv

class PLSR():
    def __init__(self, X, Y):
        # Initialize X and Y matrices
        # They are transposed due to Worlsey et al. convention
        # Rows: variables | Columns: observations
        self.X = X.T
        self.Y = Y.T
        self.cov_X = None
        self.cov_Y = None
        self.cov_XXYY = None
        self.U = None
        self.V = None
        self.C_x = None
        self.C_y = None

    
    def calculate_covariances(self):
        self.cov_X = self.X.T.dot(self.X)
        self.cov_Y = self.Y.T.dot(self.Y)
        self.cov_XXYY = self.cov_X.dot(self.cov_Y)

    
    def evaluate(self):
        """
            Calculates the weights and the main components
            associated to the PLSR.
        """
        # Get eigen vectors (X'XY'Y)A=AL
        L, A = eig(self.cov_XXYY)

        # Calculate singular values: W
        W = np.sqrt(L)

        # Select components (>95% of the information)
        W_per = np.real(W / W.sum())
        ix = np.cumsum(W_per) < 0.80

        W = np.diag(W[ix])
        A = A[:, ix]

        # Calculate B=A(A'Y'YA)^(1/2)
        S = np.diag(A.T.dot(self.cov_Y).dot(A))
        S_sq = 1 / np.sqrt(S)
        B = A.dot(np.diag(S_sq))

        # Calculate proyection matrices:
        # U = X(Y'YBW^-1)
        # v = YB
        self.U = np.real(self.X.dot(self.cov_Y).dot(B).dot(inv(W)))
        self.V = np.real(self.Y.dot(B))

        # # Calculate components (BW)' & (Y'YB)'
        # self.C_x = np.real(B.dot(W).T)
        # self.C_y = np.real(self.Y.T.dot(self.Y).dot(B).T)


    # @property
    def scores(self):
        return self.U, self.V
    
    
    # @property
    def components(self):
        return self.C_x, self.C_y
