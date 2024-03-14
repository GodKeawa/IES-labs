import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('lena.jpg')
img = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.jpeg",img)

equ = cv2.equalizeHist(img)
pic_equ = np.hstack([img,equ])
cv2.imwrite("hist_equ.jpeg",pic_equ)
cv2.imshow("Histogram Equalization",pic_equ)
cv2.waitKey(100)

plt.subplot(121)
plt.hist(img.ravel(),256,[0,256])
plt.subplot(122)
plt.hist(equ.ravel(),256,[0,256])
plt.show()
