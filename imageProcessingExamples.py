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
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)

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
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)

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
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)

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
frame1 = plt.gca()
frame1.axes.get_xaxis().set_visible(False)
frame1.axes.get_yaxis().set_visible(False)