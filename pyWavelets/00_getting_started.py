import cv2
import pywt
import numpy as np


# Load image
img = cv2.imread('files/lenna.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Start Wavelets
wp = pywt.WaveletPacket2D(data=gray, wavelet='haar', mode='symmetric')
print(wp.data)
print(repr(wp.path))
print(wp.level)
print(wp.maxlevel)

buff_a = np.concatenate((wp['a'].data, wp['h'].data), axis=1)
buff_b = np.concatenate((wp['v'].data, wp['d'].data), axis=1)

result = np.concatenate((buff_a, buff_b), axis=0)
cv2.imshow('Image', result)

while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()



