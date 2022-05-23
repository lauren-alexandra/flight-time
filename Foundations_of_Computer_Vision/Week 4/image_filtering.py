import sys
import urllib.request
import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt

URL = "https://frostlor-cdn-prod.courses.csuglobal.edu/frost/assets/images/d46f8602-a3a9-38a7-be73-46c5cdf95933/Mod4CT1.jpg"

""" Extract image """

def extract_image_from_url(url):
    # extract contents
    url_res = urllib.request.urlopen(url)
    # convert to img arr
    img_arr = np.array(bytearray(url_res.read()), dtype=np.uint8)
    # read image from a buffer in memory
    return cv.imdecode(img_arr, -1)

img = extract_image_from_url(URL)

if img is None:
    sys.exit("Could not read image.")

"""
Mean, median, and Gaussian filters (with two different values of sigma) applied using a 3x3 kernel
"""
# mean 
mean_blur_3x3 = cv.blur(img,(3,3))

# median 
median_blur_3x3 = cv.medianBlur(img,3)

# Gaussian - computed σ
# By setting sigma to 0, OpenCV computes sigma based on the kernel size: sigma = 0.3*((kernel_size-1)*0.5 - 1) + 0.8
gaussian_blur1_3x3 = cv.GaussianBlur(img,(3,3),0)

# Gaussian - σ
gaussian_blur2_3x3 = cv.GaussianBlur(img,(3,3),1)

"""
Mean, median, and Gaussian filters (with two different values of sigma) applied using a 5x5 kernel
"""
# mean 
mean_blur_5x5 = cv.blur(img,(5,5))

# median 
median_blur_5x5 = cv.medianBlur(img,5)

# Gaussian - computed σ
# By setting sigma to 0, OpenCV computes sigma based on the kernel size: sigma = 0.3*((kernel_size-1)*0.5 - 1) + 0.8
gaussian_blur1_5x5 = cv.GaussianBlur(img,(5,5),0)

# Gaussian - σ
gaussian_blur2_5x5 = cv.GaussianBlur(img,(5,5),1)

"""
Mean, median, and Gaussian filters (with two different values of sigma) applied using a 7x7 kernel
"""
# mean 
mean_blur_7x7 = cv.blur(img,(7,7))

# median 
median_blur_7x7 = cv.medianBlur(img,7)

# Gaussian - computed σ
# By setting sigma to 0, OpenCV computes sigma based on the kernel size: sigma = 0.3*((kernel_size-1)*0.5 - 1) + 0.8
gaussian_blur1_7x7 = cv.GaussianBlur(img,(7,7),0)

# Gaussian - σ
gaussian_blur2_7x7 = cv.GaussianBlur(img,(7,7),1)

"""
Plot filter results
"""
fig, axs = plt.subplots(3, 4)

# 3x3 kernel size
axs[0,0].imshow(mean_blur_3x3)
#axs[0, 0].set_title('Mean 3x3')
axs[0, 0].set(xlabel='mean', ylabel='3x3')
axs[0,1].imshow(median_blur_3x3)
#axs[0, 1].set_title('Median 3x3')
axs[0, 1].set(xlabel='median', ylabel='3x3')
axs[0,2].imshow(gaussian_blur1_3x3)
#axs[0, 2].set_title('Gaussian 3x3 - computed σ')
axs[0, 2].set(xlabel='Gaussian - computed σ', ylabel='3x3')
axs[0,3].imshow(gaussian_blur2_3x3)
#axs[0, 3].set_title('Gaussian 3x3 - σ')
axs[0, 3].set(xlabel='Gaussian - σ', ylabel='3x3')

# 5x5 kernel size
axs[1,0].imshow(mean_blur_5x5)
#axs[1, 0].set_title('Mean 5x5')
axs[1, 0].set(xlabel='mean', ylabel='5x5')
axs[1,1].imshow(median_blur_5x5)
#axs[1, 1].set_title('Median 5x5')
axs[1, 1].set(xlabel='median', ylabel='5x5')
axs[1,2].imshow(gaussian_blur1_5x5)
#axs[1, 2].set_title('Gaussian 5x5 - computed σ')
axs[1, 2].set(xlabel='Gaussian - computed σ', ylabel='5x5')
axs[1,3].imshow(gaussian_blur2_5x5)
#axs[1, 3].set_title('Gaussian 5x5 - σ')
axs[1, 3].set(xlabel='Gaussian - σ', ylabel='5x5')

# 7x7 kernel size
axs[2,0].imshow(mean_blur_7x7)
#axs[2, 0].set_title('Mean 7x7')
axs[2, 0].set(xlabel='mean', ylabel='7x7')
axs[2,1].imshow(median_blur_7x7)
#axs[2, 1].set_title('Median 7x7')
axs[2, 1].set(xlabel='median', ylabel='7x7')
axs[2,2].imshow(gaussian_blur1_7x7)
#axs[2, 2].set_title('Gaussian 7x7 - computed σ')
axs[2, 2].set(xlabel='Gaussian - computed σ', ylabel='7x7')
axs[2,3].imshow(gaussian_blur2_7x7)
#axs[2, 3].set_title('Gaussian 7x7 - σ')
axs[2, 3].set(xlabel='Gaussian - σ', ylabel='7x7')

# hide x labels and tick labels for top plots and y ticks for right plots
for ax in axs.flat:
    ax.label_outer()

plt.show()
