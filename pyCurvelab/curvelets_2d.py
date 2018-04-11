from __future__ import print_function
import os

import pyct as ct
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if __name__ == '__main__':
    print('Loading image...')
    filename = os.path.join(root, 'opencv', 'img', 'brain.jpg')
    img = imread(filename, as_grey=True)

    # Parameters
    number_of_scales = 2
    number_of_angles = 32

    # Setup curvelet params
    A = ct.fdct2(img.shape, nbs=number_of_scales, nba=number_of_angles, ac=True, norm=False, vec=True, cpx=False)

    # Apply curvelet to the image
    f = A.fwd(img)

    print('Data coefficients type: ', type(f))
    print('Coefficients array:\n\t', f)
    print('Shape: ', f.shape)
    print('Image shape vect: ', np.prod(img.shape))

    # Print Information
    for scale in range(0, number_of_scales):
        print('Scale 0: ', f(scale), '\n Shape: ', np.shape(f(scale)))

    # Reconstruct the image
    y = A.inv(f)

    fig, ax = plt.subplots(1, 2, sharey='all')
    ax[0].imshow(img, cmap='gray')
    ax[0].set_title('Original')

    ax[1].imshow(y, cmap='gray')
    ax[1].set_title('Reconstructed')
    plt.show()
