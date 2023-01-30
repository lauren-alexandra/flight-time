"""
The program detects faces in an image using the the Python Image Library.
"""

from PIL import Image, ImageDraw
import face_recognition

# load the file into a numpy array
im = face_recognition.load_image_file('./group.png')

# find face locations
face_locations = face_recognition.face_locations(im)
number_of_faces = len(face_locations)
print("Found {} face(s) in this picture.".format(number_of_faces))

# load the image into a Python Image Library object to draw on 
pil_image = Image.fromarray(im)
draw = ImageDraw.Draw(pil_image)

for face_location in face_locations:
    top, left, bottom, right = face_location
    print("A face is located at pixel location Top: {}, Left {},Bottom: {}, Right: {}".format(top, left, bottom, right))
    # draw a box around the face
    draw.rectangle([left, top, right, bottom], outline="red", width=2)

pil_image.show()
