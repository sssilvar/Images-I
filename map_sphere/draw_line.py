import numpy as np
from numpy import pi
import matplotlib.pyplot as plt


def sphere(shape=(256, 256, 256), radius=(1, 10), center=(128, 128, 128),
           theta_range=(-pi, pi), phi_range=(-pi, pi)):
    # Create variables for simplicity
    sx, sy, sz = shape
    r_min, r_max = radius
    cx, cy, cz = center
    theta_min, theta_max = theta_range
    phi_min, phi_max = phi_range

    # Define a coordinate system
    x, y, z = np.ogrid[0:sx, 0:sy, 0:sz]

    # Create an sphere in the range of r, theta and phi
    x = x - cx
    y = y - cy
    z = z - cz

    # For radius range, theta range and phi range
    eqn_mag = x ** 2 + y ** 2 + z ** 2
    eqn_theta = np.arctan2(y, x)
    eqn_theta = np.repeat(eqn_theta[:, :, np.newaxis], sz, axis=2).squeeze()

    eqn_phi = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)

    # Generate masks
    mask_radius = np.logical_and(eqn_mag > r_min ** 2, eqn_mag <= r_max ** 2)
    mask_theta = np.logical_and(eqn_theta >= theta_min, eqn_theta <= theta_max)
    mask_phi = np.logical_and(eqn_phi >= phi_min, eqn_phi <= phi_max)

    # Generate a final mask
    mask = np.logical_and(mask_radius, mask_phi)
    mask = np.logical_and(mask, mask_theta)

    return mask


def line(shape=(256, 256, 256), radius=(1, 10), center=(128, 128, 128)):
    sx, sy, sz = shape
    cx, cy, cz = center

    # Define a coordinate system
    x, y, z = np.ogrid[0:sx, 0:sy, 0:sz]

    # Create an sphere in the range of r, theta and phi
    x = x - cx
    y = y - cy
    z = z - cz

    eqn_theta = np.arctan2(y, x)
    eqn_phi = np.arctan2(y, x)


def stereo_mapping(vol: np.ndarray, center: tuple, radius=(10, 20), theta_range=(-180, 180), phi_range=(-90, 90),
                   aperture=0.2):
    sx, sy, sz = np.shape(vol)

    sph = sphere(shape=(sx, sy, sz), radius=radius, center=center)
    img = np.empty([360, 180])

    for i, angle in enumerate(range(*theta_range)):
        for j, angle in enumerate(range(*phi_range)):
            print(j)



if __name__ == '__main__':
    vol = np.random.normal(1,1, [50, 50, 50])
    center = (25, 25, 25)

    stereo_mapping(vol, center=center)
