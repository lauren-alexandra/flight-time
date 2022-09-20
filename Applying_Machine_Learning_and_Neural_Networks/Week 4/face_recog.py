#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
import face_recognition

"""
The program uses facial recognition to determine if an individual face is present in a group of faces.
"""

person_path = input("Enter the image path for the person: ")
group_path = input("Enter the image path for the group: ")

# load the images into a numpy array
person_image = face_recognition.load_image_file(person_path)
group_image = face_recognition.load_image_file(group_path)

# find face locations
face_locations = face_recognition.face_locations(group_image)
number_of_faces = len(face_locations)
print("\nFound {} face(s) in this picture.".format(number_of_faces))

# load the image into a Python Image Library object to draw on 
pil_image = Image.fromarray(group_image)
draw = ImageDraw.Draw(pil_image)

for face_location in face_locations:
    top, left, bottom, right = face_location
    print("A face is located at pixel location Top: {}, Left {},Bottom: {}, Right: {}".format(top, left, bottom, right))
    # draw a box around the face
    draw.rectangle([left, top, right, bottom], outline="red", width=2)

pil_image.show()

# find raw face landmarks in the image and return a 128-dimension face encoding
person_encoding = face_recognition.face_encodings(person_image)[0]
group_encoding = face_recognition.face_encodings(group_image, face_locations)
known_face_encodings = [person_encoding]
found_match = False

for face_encoding in group_encoding:
    # if distance between encodings is less than 0.6, match is found
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    if True in matches:
        found_match = True

if (found_match): 
    print('\nFound a match.')
else: 
    print('\nNo match found.')
