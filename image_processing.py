"""
Images are processed for facial recognition accuracy. Final images are in grayscale, adjusted for the 
effect on illumination, and rotated, cropped and scaled to create new bounding boxes for the faces. 
"""

from __future__ import print_function
import argparse
import sys
import urllib.request
import cv2 as cv
import numpy as np 

SUBJECT_1_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdkf_IPn6VW3jpJ_fTU4IUcwtGPbcvSfxXW4EPXjeVuMjM1Baz"
SUBJECT_2_URL= "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcSulLs5l2Bwr6iFywEqHxQWevj9snjLRrsPxjQWsCIrJmA9cT4q"

""" Extract images """

def extract_image_from_url(url):
    # extract contents
    url_res = urllib.request.urlopen(url)
    # convert to img arr
    img_arr = np.array(bytearray(url_res.read()), dtype=np.uint8)
    # read image from a buffer in memory
    return cv.imdecode(img_arr, -1)

subject1 = extract_image_from_url(SUBJECT_1_URL)
subject2 = extract_image_from_url(SUBJECT_2_URL)

if subject1 is None or subject2 is None:
    sys.exit("Could not read image.")

""" Convert to grayscale """

subject1 = cv.cvtColor(subject1, cv.COLOR_BGR2GRAY)
subject2 = cv.cvtColor(subject2, cv.COLOR_BGR2GRAY)

""" Resize images """

height1, width1 = subject1.shape[:2]
height2, width2 = subject2.shape[:2]

subject1 = cv.resize(subject1,(3*width1, 3*height1), interpolation = cv.INTER_CUBIC)
subject2 = cv.resize(subject2,(3*width2, 3*height2), interpolation = cv.INTER_CUBIC)

# subject images
sub1_img1 = subject1[0:519, 0:433]
sub1_img2 = subject1[0:350, 438:800]
sub2_img1 = subject2[0:519, 0:433]
sub2_img2 = subject2[0:519, 438:870]

""" Augment eyes for detection """

sub2_img2_h, sub2_img2_w = sub2_img2.shape[:2]
line_thickness = 5
# left eye coordinates
x1, y1 = 177, 241
x2, y2 = 180, 243
# left eye
cv.line(sub2_img2, (x1, y1), (x2, y2), (255, 255, 255), thickness=line_thickness)
# right eye coordinates
x10, y10 = 274, 235
x20, y20 = 280, 238
# right eye
cv.line(sub2_img2, (x10, y10), (x20, y20), (255, 255, 255), thickness=line_thickness)

""" Obtain face cascade """

parser = argparse.ArgumentParser(description='Cascades')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='\\opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt.xml')
args = parser.parse_args()
face_cascade_name = args.face_cascade
face_cascade = cv.CascadeClassifier()
# load cascade
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)

""" Detect and rotate faces """

def find_bounding_box(frame, adjust_frame=None):
    frame_gray = cv.equalizeHist(frame)
    # detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    if faces is not None:
        for (x,y,w,h) in faces:
            if adjust_frame:
                x += adjust_frame[0]
                y += adjust_frame[1]
                w += adjust_frame[2]
                h += adjust_frame[3]
            frame = cv.rectangle(frame, (x, y), (x+w,y+h),(0,0,255), 2)
            face_frame = frame[y:y+h, x:x+w]
            return face_frame 
    return frame

def rotate(img, angle): 
    rows, cols = img.shape
    center = ((cols-1)/2.0, (rows-1)/2.0)
    rotate_matrix = cv.getRotationMatrix2D(center=center, angle=angle, scale=1)
    img = cv.warpAffine(src=img, M=rotate_matrix, dsize=(cols,rows))
    return img

""" Produce bounding boxes """

sub1_img1 = rotate(sub1_img1, -10)
sub1_img1 = find_bounding_box(sub1_img1, (20, 0, -30, 0))   
sub1_img1 = cv.resize(sub1_img1, (234, 234)) 

sub1_img2 = find_bounding_box(sub1_img2)   
sub1_img2 = cv.resize(sub1_img2, (234, 234)) 

sub2_img1 = find_bounding_box(sub2_img1)   
sub2_img1 = cv.resize(sub2_img1, (234, 234)) 

sub2_img2 = find_bounding_box(sub2_img2)   
sub2_img2 = cv.resize(sub2_img2, (234, 234)) 

""" Display images """

cv.imshow('Subject 1 - Image 1', sub1_img1)
k = cv.waitKey(3000)
cv.imshow('Subject 1 - Image 2', sub1_img2)
k = cv.waitKey(3000)
cv.imshow('Subject 2 - Image 1', sub2_img1)
k = cv.waitKey(3000)
cv.imshow('Subject 2 - Image 2', sub2_img2)
k = cv.waitKey(3000)
