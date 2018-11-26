import face_recognition
from PIL import Image, ImageDraw, ImageFilter
import cv2
from func import *
cap = cv2.VideoCapture(0)

curr_key = 0
print("press '6' key for final output filter")
print("press 'esc' key to exit")
while True:
    ret, image = cap.read() #original size = 640x480
    image = cv2.resize(image, (0,0), fx=1, fy=1)
    image = image[:,:,::-1] 
    face_landmarks_list = face_recognition.face_landmarks(image)
    face_locations = face_recognition.face_locations(image)
    face_encodings = face_recognition.face_encodings(image)

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    face_number = 0
    for (top,right,bottom,left), face_encoding in zip(face_locations,face_encodings):
        fil(pil_image,draw,top,right,bottom,left,curr_key,face_landmarks_list, face_number)
        face_number += 1
# Remove the drawing library from memory as per the Pillow docs
    del draw

# Save the resulting image then display it with cv2
    pil_image.save("frame.jpg")
    frame = cv2.imread("frame.jpg")
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key != 255:
        curr_key = key
    if key == 27: #esc key
        break

cap.release()
cv2.destroyAllWindows()
"""
del draw
pil_image.show()
"""

