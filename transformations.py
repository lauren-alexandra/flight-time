import sys
import urllib.request
import cv2 as cv
import numpy as np 

URL = "https://frostlor-cdn-prod.courses.csuglobal.edu/lor/resources/src/272137f2-3816-3779-a73f-71882da43fa1/shutterstock227361781--125.jpg"

# extract contents
url_res = urllib.request.urlopen(URL)
# convert to img arr
img_arr = np.array(bytearray(url_res.read()), dtype=np.uint8)
# read image from a buffer in memory
img = cv.imdecode(img_arr, -1)

if img is None:
    sys.exit("Could not read the image.")

height, width = img.shape[:2]
# img.shape = (83, 125, 3)

""" Scale """

resized_img = cv.resize(img,(5*width, 5*height), interpolation = cv.INTER_CUBIC)
# resized_img.shape = (415, 625, 3)
cv.imwrite("banknotes.png", resized_img)

""" Rotate and adjust color """

features = resized_img[100:500, 20:300]
rows, cols, clrs = features.shape

# the center coordinates of the image
# cols-1 and rows-1 are the coordinate limits
center = ((cols-1)/2.0, (rows-1)/2.0)

# the transformation matrix
rotate_matrix = cv.getRotationMatrix2D(center=center, angle=270, scale=1)
"""
[[-1.8369702e-16 -1.0000000e+00  2.9650000e+02]
 [ 1.0000000e+00 -1.8369702e-16  1.7500000e+01]]
"""

features = cv.warpAffine(src=features, M=rotate_matrix, dsize=(cols,rows))

# set all blue pixels to zero to highlight the bell in the inkwell and color-shifting 100
features[:, :, 0] = 0 

cv.imwrite("features.png", features)
cv.imshow('Display window', features)
k = cv.waitKey(0)
