import cv2
from flask_opencv_streamer.streamer import Streamer
from gpiozero import LED, Servo
import time

servo = Servo(18)
laser = LED(23)

port = 3030
require_login = False
streamer = Streamer(port, require_login)

cap = cv2.VideoCapture(0)
faceCas = cv2.CascadeClassifier('face.xml')

rValue = 10

laser.on()


try:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)

        faces = faceCas.detectMultiScale(frame, 1.1, 4)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        try:
            if faces.any() and rValue >= 10:
                servo.value = 0.1
                time.sleep(1)
                servo.value = 0.9
                time.sleep(1)
                servo.value = 1
                time.sleep(1)
                servo.value = -1
                rValue = 1
        except AttributeError:
            pass

        if rValue < 10:
            rValue += .2

        if cv2.waitKey(1) == ord('q'):
            break

        streamer.update_frame(frame=frame)

        if not streamer.is_streaming:
            streamer.start_streaming()
except KeyboardInterrupt:
    laser.off()
    exit()
