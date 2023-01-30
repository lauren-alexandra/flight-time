"""
Image is processed using morphological operations (dilation, erosion, opening, and closing)
"""

import cv2 as cv
import numpy as np 

# convert to grayscale
img = cv.imread('cursive.jpg', cv.IMREAD_GRAYSCALE)
# convert to binary image
(thresh, binary_img) = cv.threshold(img, 127, 255, cv.THRESH_BINARY_INV)
cv.imwrite("cursive_binary.jpg", binary_img)

# structuring element
kernel = np.ones((5,5), np.uint8)

# erode operation (2x)
erosion = cv.erode(binary_img, kernel, iterations = 2)
cv.imwrite("cursive_erosion.jpg", erosion)

# dilate operation (2x)
dilation = cv.dilate(binary_img, kernel, iterations = 2)
cv.imwrite("cursive_dilation.jpg", dilation)

# opening operation (2x)
opening = cv.morphologyEx(binary_img, cv.MORPH_OPEN, kernel, iterations = 2)
cv.imwrite("cursive_opening.jpg", opening)

# closing operation (2x)
closing = cv.morphologyEx(binary_img, cv.MORPH_CLOSE, kernel, iterations = 2)
cv.imwrite("cursive_closing.jpg", closing)
