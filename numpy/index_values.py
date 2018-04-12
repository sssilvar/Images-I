import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    print('Creating volume...')
    x = np.zeros([256, 256, 256])

    print('Setting ones')
    x[100:150, 100:150, 100:150] = 1

    # Find the ones
    ix = np.where(x == 1)
    print('Indexes: ', ix)
    print(np.sum(x[ix]))

    # Plot x
    plt.imshow(x[:, :, 128], cmap='gray')
    plt.show()
