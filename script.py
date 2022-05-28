# This program will is written for the purposes of security
# Using the cv2 module, it will detect a person using the camera and start recording.
# The recording will be stored in the working directory of this program
# Written by Timothy Nkata

from pickle import TRUE
#from tkinter import N
from charset_normalizer import detect
import cv2
import sys
import time
import datetime

from sqlalchemy import false, true

cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False # initialized with False as nothing has been found yet
detection_stopped_time = None
timer_stopped = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v") #four character code for mp4 video format

out = cv2.VideoWriter("video.mp4", fourcc, 20, frame_size)

while True:
    _, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # x y widht and height of faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0: # Face or body detected
        if detection:
            timer_started = False
        else: #Start a new video to record
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%m-%S")
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("Started recording!")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stopped Recording!")
        else:
            timer_started = True
            detection_stopped_time = time.time()

    
    if detection:
        out.write(frame)
    #for (x, y, width, height) in faces:
    #    cv2.rectangle(frame, (x,y), (x + width, y + height), (255, 0, 0), 3)

    #for (x, y, width, height) in bodies:
    #    cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)



    cv2.imshow("Camera", frame) # comment this out to remove pop up recording

    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()