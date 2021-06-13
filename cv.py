from flask_opencv_streamer.streamer import Streamer
import cv2
import time
from gpiozero import LED

port = 3030
require_login = False
streamer = Streamer(port, require_login)

faceCas = cv2.CascadeClassifier('face.xml')

led = LED(18)

cap = cv2.VideoCapture(0)

background = cv2.imread('IMG_6375.jpg')
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background = cv2.GaussianBlur(background, (21, 21), 0)
background = cv2.resize(background, (500, 500))

while True:
    ret, frame = cap.read()

    frame = cv2.resize(frame, (500, 500))

    faces = faceCas.detectMultiScale(frame, 1.1, 4)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    diff = cv2.absdiff(background, gray)

    cnts, res = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in cnts:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        led.on()
        time.sleep(1)
        led.off()

    streamer.update_frame(frame)

    if not streamer.is_streaming:
        streamer.start_streaming()

    cv2.waitKey(1)
