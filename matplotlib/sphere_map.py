from mayavi import mlab
import numpy as np
import cv2

def test_mesh():
    """A very pretty picture of spherical harmonics translated from
    the octaviz example."""
    pi = np.pi
    cos = np.cos
    sin = np.sin
    dphi, dtheta = pi / 250.0, pi / 250.0
    [phi, theta] = np.mgrid[0:pi + dphi * 1.5:dphi,
                               0:2 * pi + dtheta * 1.5:dtheta]
    r = 1
    x = r * sin(phi) * cos(theta)
    y = r * cos(phi)
    z = r * sin(phi) * sin(theta)

    return mlab.mesh(x, y, z, colormap="bone")


if __name__ == '__main__':
    test_mesh()
    mlab.show()