from __future__ import print_function
import os

import pyct as ct
from skimage.io import imread
import matplotlib.pyplot as plt

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    print('Loading image...')
    filename = os.path.join(root, 'opencv', 'img', 'brain.jpg')
    img = imread(filename, as_grey=True)

    # Setup curvelet params
    A = ct.fdct2(img.shape, nbs=6, nba=64, ac=True, norm=False, vec=True, cpx=False)

    # Apply curvelet to the image
    f = A.fwd(img)

    print('Coefficients array:\n\t', f)
    print('Shape: ', f.shape)

    plt.imshow(img)
    plt.show()
