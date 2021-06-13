from flask_opencv_streamer.streamer import Streamer
import cv2
import time
from gpiozero import Buzzer

port = 3030
require_login = False
streamer = Streamer(port, require_login)

faceCas = cv2.CascadeClassifier('face.xml')


cap = cv2.VideoCapture(0)

alarm = Buzzer(18)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 0)

    faces = faceCas.detectMultiScale(frame, 1.1, 4)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)
        alarm.on()
        time.sleep(1)
        alarm.off()
        
    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()

    cv2.waitKey(1)
