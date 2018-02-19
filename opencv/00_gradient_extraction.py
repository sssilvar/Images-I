import cv2
import os
import matplotlib.pyplot as plt


# Define parameters
img_file = os.path.join(os.getcwd(), 'img', 'brain.jpg')
# Read image
img = cv2.imread(img_file, 0)

# plt.imshow(img)
# plt.show()

# # Apply filter
# edges = cv2.Laplacian(img, cv2.CV_64F)
#
# cv2.imwrite('test.jpg', edges)

