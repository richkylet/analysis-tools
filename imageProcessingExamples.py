'''
Example code for image processing techniques

----------
KTR 2016
'''


#===============================
import numpy as np
from scipy import signal, misc
import matplotlib.pyplot as plt

plt.close("all")
#===============================

# original image: ==============
image = misc.ascent().astype(np.float32)

plt.figure(3)
plt.subplot(2,2,1)
plt.imshow(image)
plt.gray()
plt.title('Original')
plt.show()

# spline filtering (edge detection) ========================
derfilt = np.array([1.0, -2, 1.0], dtype=np.float32)
ck = signal.cspline2d(image, 8.0)
new_image = (signal.sepfir2d(ck, derfilt, [1]) + signal.sepfir2d(ck, [1], derfilt))

plt.figure(3)
plt.subplot(2,2,2)
plt.imshow(new_image)
plt.gray()
plt.title('Spline (edge filter)')
plt.show()


# convolution  (shift-invariance) ==============
image = misc.ascent()

w = np.zeros((50, 50))
w[0][0] = 2.0
w[49][25] = 1.2
image_new = signal.fftconvolve(image, w)

plt.figure(3)
plt.subplot(2,2,3)
plt.imshow(image_new)
plt.gray()
plt.title('fft-convolved (shift)')
plt.show()

# Guassian filtering (blurring) ==============
image = misc.ascent()

w = signal.gaussian(50, 10.0)
image_new = signal.sepfir2d(image, w, w)

plt.figure(3)
plt.subplot(2,2,4)
plt.imshow(image_new)
plt.gray()
plt.title('guass-filtered (blurred)')
plt.show()