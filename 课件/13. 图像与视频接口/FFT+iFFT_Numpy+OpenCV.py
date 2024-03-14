import cv2
import numpy as np
from matplotlib import pyplot as plt

def magnitude(x,y):
    x_m = x*x
    y_m = y*y
    z_m = x_m + y_m
    return np.sqrt(z_m)

# Numpy
img1 = cv2.imread("lena.jpg")
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)

f = np.fft.fft2(img)
#print img
f_shift = np.fft.fftshift(f)
magnitude_spectrum1 = 20 * np.log10(np.abs(f_shift))
#print "image:",img

ph_f = np.angle(f)
ph_fshift = np.angle(f_shift)

# iFFT
f1shift = np.fft.ifftshift(f_shift)
img_back1 = np.fft.ifft2(f1shift)
img_back = np.abs(img_back1)

plt.subplot(241),plt.imshow(img, cmap = "gray")
plt.title("Input image"),plt.xticks([]),plt.yticks([])
plt.subplot(242),plt.imshow(magnitude_spectrum1, cmap="gray")
plt.title("Numpy fft2 image_amp"),plt.xticks([]),plt.yticks([])
plt.subplot(243),plt.imshow(ph_fshift, cmap="gray")
plt.title("Numpy fft2 image_phase"),plt.xticks([]),plt.yticks([])
plt.subplot(244),plt.imshow(img_back, cmap="gray")
plt.title("image back"),plt.xticks([]),plt.yticks([])

# OpenCV
dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)
magnitude_spectrum2 = 20 * np.log10(magnitude(dft_shift[:,:,0], dft_shift[:,:,1]))


# iFFT
dft_ishift = np.fft.ifftshift(dft_shift)
img_back2 = cv2.idft(dft_ishift)
img_back3 = cv2.magnitude(img_back2[:,:,0],img_back2[:,:,1])

plt.subplot(245),plt.imshow(img, cmap="gray")
plt.title("Input image"), plt.xticks([]),plt.yticks([])
plt.subplot(246), plt.imshow(magnitude_spectrum2, cmap="gray")
plt.title("DFT image"), plt.xticks([]), plt.yticks([])
plt.subplot(248),plt.imshow(img_back3, cmap="gray")
plt.title("image back"),plt.xticks([]),plt.yticks([])
plt.show()
