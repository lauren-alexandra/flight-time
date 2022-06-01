"""
Adaptive thresholding schemes segment three different images. 
"""

import cv2 as cv
import numpy as np 
from matplotlib import pyplot as plt

""" Load and prepare images """

outdoor = cv.imread('outdoor.png')
indoor = cv.imread('indoor.png')
close_up = cv.imread('close_up.png')

# convert to grayscale
outdoor_gray = cv.cvtColor(outdoor, cv.COLOR_BGR2GRAY)
indoor_gray = cv.cvtColor(indoor, cv.COLOR_BGR2GRAY)
close_up_gray = cv.cvtColor(close_up, cv.COLOR_BGR2GRAY)

# filter
outdoor_gray = cv.GaussianBlur(outdoor_gray,(5,5),0)
indoor_gray = cv.medianBlur(indoor_gray,5)
close_up_gray = cv.GaussianBlur(close_up_gray,(5,5),0)

""" Adaptive thresholding """

# the threshold value is a gaussian-weighted sum of the neighbourhood values minus the constant C
outdoor_th = cv.adaptiveThreshold(outdoor_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,9,3)
# the threshold value is the mean of the neighbourhood area minus the constant C
indoor_th = cv.adaptiveThreshold(indoor_gray,255,cv.ADAPTIVE_THRESH_MEAN_C,\
            cv.THRESH_BINARY,11,2)
close_up_th = cv.adaptiveThreshold(close_up_gray,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv.THRESH_BINARY,7,2)

fig, ((ax1, ax2, ax3), (ax10, ax20, ax30)) = plt.subplots(nrows = 2, ncols = 3, figsize = (15,10))
imgs = [outdoor, indoor, close_up, outdoor_th, indoor_th, close_up_th]
titles = ['Outdoor', 'Indoor', 'Close up', 'Outdoor - Thresh', 'Indoor - Thresh', 'Close up - Thresh']
axs = [ax1, ax2, ax3, ax10, ax20, ax30]

for i, ax in enumerate(axs):
    ax.imshow(cv.cvtColor(imgs[i], cv.COLOR_BGR2RGB))
    ax.axis('off')
    ax.set_title(titles[i])

plt.show()
