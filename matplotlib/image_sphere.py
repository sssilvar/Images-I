import numpy as np
from mayavi import mlab
import cv2

# Read image
img = cv2.imread('/home/sssilvar/Downloads/download.jpeg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# img = np.random.normal(255, 200, (500, 500))


vmin = 0
vmax = img.max()

# size of the grid
x_size = 318
y_size = 159

theta = np.linspace(np.pi, 0, y_size)
phi   = np.linspace(-np.pi, np.pi, x_size)
longitude = np.radians(np.linspace(-180, 180, x_size))
latitude = np.radians(np.linspace(-90, 90, y_size))

# project the map to a rectangular matrix xsize x ysize
PHI, THETA = np.meshgrid(phi, theta)

# Create a sphere
r = 0.3
x = r*np.sin(THETA)*np.cos(PHI)
y = r*np.sin(THETA)*np.sin(PHI)
z = r*np.cos(THETA)


# Plot it!
mlab.figure(1, bgcolor=(1, 1, 1), fgcolor=(0, 0, 0), size=(400, 300))
mlab.clf()

mlab.mesh(x, y, z, scalars=img, colormap="jet", vmin=vmin, vmax=vmax)

cv2.imshow('Image', img)
mlab.show()

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
