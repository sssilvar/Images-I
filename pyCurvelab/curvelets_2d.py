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
    A = ct.fdct2(img.shape, nbs=2, nba=64, ac=True, norm=False, vec=True, cpx=False)

    # Apply curvelet to the image
    f = A.fwd(img)

    print('Coefficients array:\n\t', f)
    print('Shape: ', f.shape)

    # Reconstruct the image
    y = A.inv(f)

    fig, ax = plt.subplots(1, 2, sharey='all')
    ax[0].imshow(img, cmap='gray')
    ax[0].title('Original')

    ax[1].imshow(y, cmap='gray')
    ax[1].title('Reconstructed')
    plt.show()
