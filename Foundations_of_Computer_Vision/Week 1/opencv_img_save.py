import sys
import urllib.request
import cv2 as cv
import numpy as np 

URL = "https://frostlor-cdn-prod.courses.csuglobal.edu/lor/resources/src/7985e0c1-89b3-35e6-b709-8c90e828356c/shutterstock93075775--250.jpg"

# extract contents
url_res = urllib.request.urlopen(URL)
# convert to img arr
img_arr = np.array(bytearray(url_res.read()), dtype=np.uint8)
# read image from a buffer in memory
img = cv.imdecode(img_arr, -1)

if img is None:
    sys.exit("Could not read the image.")

# displays image in the specified window
cv.imshow('Display window', img)
# waits for a pressed key: 0 is the special value that means "forever"
k = cv.waitKey(0)

# saves on "s" key
if k == ord("s"):
    # saves an image to a specified file
    cv.imwrite("brain.png", img)
