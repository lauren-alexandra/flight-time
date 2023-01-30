"""
Description: The program detects faces in images and applies blurring to eyes.
"""

import argparse
import cv2 as cv
import numpy as np 

""" Convert to grayscale """

img1 = cv.imread('img1.png', cv.IMREAD_GRAYSCALE)
img2 = cv.imread('img2.png', cv.IMREAD_GRAYSCALE)
img3 = cv.imread('img3.png', cv.IMREAD_GRAYSCALE)

""" Rotate """

def rotate(img, angle): 
    rows, cols = img.shape
    center = ((cols-1)/2.0, (rows-1)/2.0)
    rotate_matrix = cv.getRotationMatrix2D(center=center, angle=angle, scale=1)
    img = cv.warpAffine(src=img, M=rotate_matrix, dsize=(cols,rows))
    return img

img3 = rotate(img3, 10)

""" Obtain cascades """

parser = argparse.ArgumentParser(description='Face and eye cascades')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='opencv\\sources\\data\\haarcascades\\haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='opencv\\sources\\data\\haarcascades\\haarcascade_eye_tree_eyeglasses.xml')
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
    
# load cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

""" Detect faces and eyes """

def detect(frame, find_eyes=False):
    frame_gray = cv.equalizeHist(frame)
    # detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    face_frames = [] 

    if faces is not None:
        for face in faces:
            (x, y, w, h) = face
            frame_cp = np.copy(frame)
            cv.rectangle(frame_cp, (x, y), (x+w,y+h),(0,0,255), 2)
            face_frames.append(frame_cp[y:y+h, x:x+w])

            if find_eyes:
                faceROI = frame_cp[y:y+h,x:x+w]
                # detect eyes
                eyes = eyes_cascade.detectMultiScale(faceROI)

                for (x2,y2,w2,h2) in eyes:
                    eye = faceROI[y2+7:y2+7+h2, x2-5:x2-5+w2+7] 
                    # blur eyes
                    for i in range(15):
                        eye = cv.medianBlur(eye,7) 
                    faceROI[y2+7:y2+7+h2, x2-5:x2-5+w2+7] = eye
                    face_frames.append(faceROI)

    return face_frames

""" Retrieve all faces """

img1_ff = detect(img1)
img2_ff= detect(img2)
img3_ff = detect(img3)

""" Scale images """

scaled_frames = []
f_frames = [img1_ff, img2_ff, img3_ff]
for fr_set in f_frames: 
    for f in fr_set:
        h, w = f.shape[:2]
        if h < 100: 
            resized_frame = cv.resize(f,(2*w, 2*h), interpolation = cv.INTER_CUBIC)
        else:
            resized_frame = cv.resize(f,(w//2, h//2), interpolation = cv.INTER_CUBIC)
        scaled_frames.append(resized_frame)

""" Display images """

for f in range(len(scaled_frames)): 
    blurred_eye_frames = detect(scaled_frames[f], find_eyes=True)
    for b in blurred_eye_frames:
        cv.imshow('Face with blurred eyes', b)
        k = cv.waitKey(3000)
        cv.imwrite(f'Face_{str(f)}.png', b)
