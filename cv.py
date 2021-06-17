import cv2
from flask_opencv_streamer.streamer import Streamer
from gpiozero import LED, Servo
import time

laser = LED(23)

port = 3030
require_login = False
streamer = Streamer(port, require_login)

cap = cv2.VideoCapture(0)
faceCas = cv2.CascadeClassifier('face.xml')

servoValue = 1
decrementValue = .1
rValue = 5

rValue = 10   # Restricts stuff at a given point.

laser.on()


try:
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 0)

        faces = faceCas.detectMultiScale(frame, 1.1, 4)

        for x, y, w, h in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if x < 300:
                if servoValue > .2:
                    servo = Servo(18)
                    servoValue -= .1
                    time.sleep(.30)
                    servo.value = servoValue
                    time.sleep(1)
                
                    servo.detach()
                    servo = None

            elif x > 300:
                if servoValue < .8:
                    servo = Servo(18)
                    servoValue += .1
                    time.sleep(.30)
                    servo.value = servoValue
                    time.sleep(1)
                
                    servo.detach()
                    servo = None

            cutOffSValue = str(servoValue)[:3]
            cutOffSValue = float(cutOffSValue)

        if cv2.waitKey(1) == ord('q'):
            break

        streamer.update_frame(frame=frame)

        if not streamer.is_streaming:
            streamer.start_streaming()
except KeyboardInterrupt:
    laser.off()
    exit()
