import os

import numpy as np
from numpy import pi
import matplotlib.pyplot as plt
from scipy.ndimage.measurements import center_of_mass

import nibabel as nb


def sph2cart(r, az, el):
    rcos_theta = r * np.cos(el)
    x = rcos_theta * np.cos(az)
    y = rcos_theta * np.sin(az)
    z = r * np.sin(el)
    return x, y, z


def get_centroid(mat):
    """
    Gets the center of mass coordinates of a n-dimensional matrix
    :param mat: nd-array
    :return: tuple, or list of tuples.
        Coordinates of centers-of-mass.
    """
    centroid_coordinates = np.ceil(center_of_mass(mat)).astype(np.int)
    return tuple(centroid_coordinates)


def extract_sub_volume(vol, radius, centroid):
    cx, cy, cz = centroid
    cx_min, cx_max = (cx - radius[1], cx + radius[1])
    cy_min, cy_max = (cy - radius[1], cy + radius[1])
    cz_min, cz_max = (cz - radius[1], cz + radius[1])

    vol_sub = vol[cx_min:cx_max, cy_min:cy_max, cz_min:cz_max]
    center = (int((cx_max - cx_min) / 2), int((cy_max - cy_min) / 2), int((cz_max - cz_min) / 2))

    return vol_sub, center


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


def line(shape=(256, 256, 256), radius=(128, 128, 128), center=(128, 128, 128), angle=(90, 90)):
    sx, sy, sz = shape
    cx, cy, cz = center
    theta, phi = angle

    r_min, r_max = radius

    theta = np.deg2rad(theta)
    phi = np.deg2rad(phi)

    # Define a coordinate system
    x, y, z = np.ogrid[0:sx, 0:sy, 0:sz]

    # Create an sphere in the range of r, theta and phi
    x = x - cx
    y = y - cy
    z = z - cz

    eqn_r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
    eqn_theta = np.arctan2(y, x)
    eqn_phi = np.arctan2(np.sqrt(x ** 2 + y ** 2), z)

    mask = np.logical_and(
        np.isclose(eqn_theta, theta * np.ones_like(eqn_theta), rtol=0.05),
        np.isclose(eqn_phi, phi * np.ones_like(eqn_phi), rtol=0.05))

    mask = np.logical_and(
        mask,
        np.logical_and(eqn_r >= r_min, eqn_r <= r_max))

    return mask


def stereo_mapping(vol: np.ndarray, center: tuple, radius=(10, 20), theta_range=(-180, 180), phi_range=(0, 180)):
    sx, sy, sz = np.shape(vol)

    # Create sphere (scale)
    sph = sphere(shape=(sx, sy, sz), radius=radius, center=center)
    plt.imshow(sph[:, :, center[2]])
    plt.show()
    img = np.empty([360, 180])

    print('[  INFO  ] Starting mapping...')
    for i, theta in enumerate(range(*theta_range)):
        for j, phi in enumerate(range(*phi_range)):
            mask = line(shape=(sx, sy, sz), radius=radius, center=center, angle=(theta, phi))
            vol_masked = vol * mask

            # Number of voxels: n
            n = mask.sum()

            # Get mean
            img[i, j] = np.nan_to_num(vol_masked.sum() / n)
        print('\t Mapping (%d, %d)' % (i, j))
    print('[  OK  ] Mapping done!')
    return img


if __name__ == '__main__':
    subject_folder = '/user/ssilvari/home/Downloads'
    aseg_file = os.path.join(subject_folder, 'aseg.mgz')
    bmask_file = os.path.join(subject_folder, 'brainmask_reg.mgz')

    # Load volumes
    aseg = nb.load(aseg_file).get_data()
    vol = nb.load(bmask_file).get_data()

    # get centroid
    centroid = get_centroid(aseg != 0)
    print('[  INFO  ] Centroid located at: ', centroid)

    # Extract gradients
    gx, gy, gz = np.gradient(vol)
    g_mag = np.nan_to_num(np.sqrt(gx ** 2 + gy ** 2 + gz ** 2))

    # Start mapping
    radius = (15, 20)
    sub_mag, centroid = extract_sub_volume(g_mag, radius=radius, centroid=centroid)
    img_mapped = stereo_mapping(sub_mag, center=centroid, radius=radius)
    plt.imsave('/user/ssilvari/home/Downloads/temp/mapped_%d_to_%d.png' % radius, img_mapped, cmap='gray')
