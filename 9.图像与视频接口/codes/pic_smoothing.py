# coding=utf-8  

import cv2
import numpy as np
from matplotlib import pyplot as plt

####################################  
# BGR to RGB
def bgr2rgb(src):
    img = src.copy()
    img[:,:,0] = src[:,:,2]
    img[:,:,2] = src[:,:,0]
    return img
######################################  

img = cv2.imread("smooth.jpg")

# 创建掩膜  
k = 9
kernel = np.ones((k,k), np.float32)/k**2
#print kernel

# 均值滤波
img_average = cv2.filter2D(img,-1,kernel)

# 使用blur()函数进行均值滤波
img_blur = cv2.blur(img, (k,k))

# 高斯平滑  
img_gaussian = cv2.GaussianBlur(img, (k,k), 3)


# 中值滤波  
img_median = cv2.medianBlur(img,k)

img_laplace = cv2.Laplacian(img,-1)

# 平滑滤波结果  
plt.subplot(231),plt.imshow(bgr2rgb(img),"gray"),plt.title("Original")
plt.xticks([]),plt.yticks([])  # 去掉坐标轴刻度  
plt.subplot(232),plt.imshow(bgr2rgb(img_average),"gray"),plt.title("average_filtering")
plt.xticks([]),plt.yticks([])
plt.subplot(233),plt.imshow(bgr2rgb(img_gaussian),"gray"),plt.title("gaussian_filtering")
plt.xticks([]),plt.yticks([])
plt.subplot(235),plt.imshow(bgr2rgb(img_median),"gray"),plt.title("median_filtering")
plt.xticks([]),plt.yticks([])
plt.subplot(236),plt.imshow(bgr2rgb(img_laplace),"gray"),plt.title("laplace_filtering")
plt.xticks([]),plt.yticks([])
plt.show()
