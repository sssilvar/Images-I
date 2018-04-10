from __future__ import print_function

import pyct as ct
from skimage.io import imread
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('Loading image...')
    img = imread('../opencv/img/brain.jpg')

    plt.imshow(img)
    plt.show()
