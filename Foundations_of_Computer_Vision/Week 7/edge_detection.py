import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

GREEN = (0, 255, 0)
BLUE = (255, 0, 0)
RED = (0, 0, 255)
YELLOW = (0, 255, 255)

# corner points
p0 = 100, 30
p1 = 300, 210

# image with black background
img = np.zeros((300, 600, 3), np.uint8)
cv.rectangle(img, p0, p1, GREEN, cv.FILLED)
cv.circle(img, (450, 120), 70, BLUE, -1)
cv.imwrite("synthetic_img.jpg", img)

# Experiment 1

# apply canny
canny_edges = cv.Canny(img, 100, 200)

# apply sobel 
sobelx = cv.Sobel(img, cv.CV_32F, 1, 0)  # kernel for x-axis
sobely = cv.Sobel(img, cv.CV_32F, 0, 1)  # kernel for y-axis
 
# apply laplacian
laplacian = cv.Laplacian(img, cv.CV_32F)
laplacian_edge = img - laplacian

fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(nrows = 2, ncols = 3, figsize = (10,5))
 
# when showing images in matplotlib, convert image from BGR to RGB
ax1.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
ax1.set_title('Original')
ax2.imshow(cv.cvtColor(canny_edges, cv.COLOR_BGR2RGB))
ax2.set_title('Canny')
ax3.imshow(cv.cvtColor(sobelx, cv.COLOR_BGR2RGB))
ax3.set_title('Sobel X')
ax4.imshow(cv.cvtColor(sobely, cv.COLOR_BGR2RGB))
ax4.set_title('Sobel Y')
ax5.imshow(cv.cvtColor(laplacian_edge, cv.COLOR_BGR2RGB))
ax5.set_title('Laplacian')

plt.show()

# Experiment 2

# image with white background
img2 = np.full((300, 600), 255, np.uint8)
cv.rectangle(img2, p0, p1, RED, cv.FILLED)
cv.circle(img2, (450, 120), 70, YELLOW, -1)

# introduce Gaussian noise
mean = 0
sigma = 0.1
gaussian = np.random.normal(mean, sigma, (300, 600)) 
gaussian_image = img2 + gaussian
noisy_image = gaussian_image.astype(np.uint8)

# apply canny
canny_edges2 = cv.Canny(noisy_image, cv.CV_32F, 100, 200)

# apply sobel 
sobelx2 = cv.Sobel(noisy_image, cv.CV_32F, 1, 0)  # kernel for x-axis
sobely2 = cv.Sobel(noisy_image, cv.CV_32F, 0, 1)  # kernel for y-axis
 
# apply laplacian
laplacian2 = cv.Laplacian(noisy_image, cv.CV_32F)
laplacian_edge2 = noisy_image - laplacian2

fig, ((ax12, ax22, ax32), (ax42, ax52, ax62)) = plt.subplots(nrows = 2, ncols = 3, figsize = (10,5))
 
ax12.imshow(cv.cvtColor(noisy_image, cv.COLOR_BGR2RGB))
ax12.set_title('Original 2')
ax22.imshow(cv.cvtColor(canny_edges2, cv.COLOR_BGR2RGB))
ax22.set_title('Canny')
ax32.imshow(cv.cvtColor(sobelx2, cv.COLOR_BGR2RGB))
ax32.set_title('Sobel X')
ax42.imshow(cv.cvtColor(sobely2, cv.COLOR_BGR2RGB))
ax42.set_title('Sobel Y')
ax52.imshow(cv.cvtColor(laplacian_edge2, cv.COLOR_BGR2RGB))
ax52.set_title('Laplacian')

plt.show()
cv.waitKey(0)
cv.destroyAllWindows()
