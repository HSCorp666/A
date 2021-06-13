from flask_opencv_streamer.streamer import Streamer
from gpiozero import LED
import cv2
import time

port = 3030
require_login = False
streamer = Streamer(port, require_login)

faceCas = cv2.CascadeClassifier('face.xml')


cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)

    faces = faceCas.detectMultiScale(1.1, 4)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        LED.on()
        time.sleep(1.5)
        LED.off()

    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()

    cv2.waitKey(1)
