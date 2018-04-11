from __future__ import print_function

import pyct as ct
from skimage.io import imread
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('Loading image...')
    img = imread('../opencv/img/brain.jpg', as_grey=True)

    # Setup curvelet params
    A = ct.fdtc(img.shape, nbs=2, nba=32, ac=True, norm=False, vec=True, cpx=False)

    # Apply curvelet to the image
    f = A.fwd(img)

    print('Coefficients array:\n\t', f)
    print('Shape: ', f.shape)

    plt.imshow(img)
    plt.show()
