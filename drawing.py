from __future__ import print_function
import argparse
import cv2 as cv

img = cv.imread('profile.jpg')

parser = argparse.ArgumentParser(description='Face and eye cascades')
parser.add_argument('--face_cascade', help='Path to face cascade.', default='data\\haarcascades\\haarcascade_frontalface_alt.xml')
parser.add_argument('--eyes_cascade', help='Path to eyes cascade.', default='data\\haarcascades\\haarcascade_eye_tree_eyeglasses.xml')
args = parser.parse_args()
face_cascade_name = args.face_cascade
eyes_cascade_name = args.eyes_cascade
face_cascade = cv.CascadeClassifier()
eyes_cascade = cv.CascadeClassifier()
    
# load the cascades
if not face_cascade.load(cv.samples.findFile(face_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)
if not eyes_cascade.load(cv.samples.findFile(eyes_cascade_name)):
    print('--(!)Error loading eyes cascade')
    exit(0)

def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    # detect faces
    faces = face_cascade.detectMultiScale(frame_gray)
    for (x,y,w,h) in faces:
        center = (x + w//2, y + h//2)
        frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (128, 255, 0), 4)
        faceROI = frame_gray[y:y+h,x:x+w]
        cv.putText(img, str('this is me'), (x+70,y-10), cv.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        # in each face, detect eyes
        eyes = eyes_cascade.detectMultiScale(faceROI)

        roi_color = img[y:y+h, x:x+w]
        for (x2,y2,w2,h2) in eyes:
            frame = cv.rectangle(roi_color, (x2,y2),(x2+w2,y2+h2),(0,0,255),2)

    cv.imshow('Face and eyes detected', img)
    k = cv.waitKey(3000)


detectAndDisplay(img)    
cv.imwrite("face_detected.png", img)
