"""
Title: Puppy Image Multi-scale Representation
Description: An image is imported. BGR channels are extracted to create 2D images and the images are merged back into a colored 3D image.
2D images are merged back together into another 3D image, swapping out the red channel with the green channel.
"""

import sys
import urllib.request
import cv2 as cv
import numpy as np 

URL = "https://frostlor-cdn-prod.courses.csuglobal.edu/lor/resources/src/89f79919-379b-3a8f-997a-98f3dd1d3a8a/shutterstock215592034--250.jpg"

# extract contents
url_res = urllib.request.urlopen(URL)
# convert to img arr
img_arr = np.array(bytearray(url_res.read()), dtype=np.uint8)
# read image from a buffer in memory
img = cv.imdecode(img_arr, -1)

if img is None:
    sys.exit("Could not read the image.")

cv.imwrite("puppy.png", img)
# img.shape = (257, 250, 3)

# extract channels
b,g,r = cv.split(img)
# b.shape, g.shape, r.shape = (257, 250)
cv.imwrite("puppy_B.png", b)
cv.imwrite("puppy_G.png", g)
cv.imwrite("puppy_R.png", r)

# merge images back into a colored 3D image
BGR_img = cv.merge((b,g,r))
cv.imwrite("puppy_BGR.png", BGR_img)

# swap out the red channel with the green channel (GRB)
GRB_img = cv.merge((g,r,b))
cv.imwrite("puppy_GRB.png", GRB_img)
