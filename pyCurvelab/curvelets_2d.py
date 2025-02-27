from __future__ import print_function
import os
import sys

import pyct as ct
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def print_cl_info(f, scale, angle):
    try:
        data = f(scale, angle)
        print('Scale %d / angle %d: ' % (scale, angle),
              '\t Shape: ', np.shape(data))
    except IndexError:
        print('[  ERROR  ] Index (%d, %d) out of range' % (scale, angle))


if __name__ == '__main__':
    print('Loading image...')
    filename = os.path.join(root, 'pyCurvelab', 'test', 'gradient_020_to_025_solid_angle_to_sphere.png')
    img = imread(filename, as_grey=True)

    # Parameters
    th = int(sys.argv[1])
    number_of_scales = 7
    number_of_angles = 16

    for s in range(0, number_of_scales):
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
            if scale == 0:
                angles = [0]
            elif scale == 1:
                angles = range(0, number_of_angles)
            elif scale % 2 == 0:
                angles = range(0, int(scale * number_of_angles))
            elif scale % 2 != 0:
                angles = range(0, int((scale - 1) * number_of_angles))
            else:
                angles = []
                raise ValueError('There is no angles inside the scale')

            # Go over all the angles in the scale
            for angle in angles:
                if scale != th:
                    ix = A.index(scale)
                    # Delete data for testing
                    f[ix[0]:ix[1]] = 0
                    print('Index: ', ix)
                print_cl_info(f, scale, angle)

        # Reconstruct the image
        y = A.inv(f)

        fig, ax = plt.subplots(1, 2, sharey='all')
        ax[0].imshow(img, cmap='gray')
        ax[0].set_title('Original')

        ax[1].imshow(np.abs(y), cmap='gray')
        ax[1].set_title('Reconstructed (Only scale %d)' % th)
        plt.savefig(os.path.join('/home/sssilvar/Documents/output/', 'scale_%d_removed.png' % s), bbox_inches='tight')
        plt.show()
        break
