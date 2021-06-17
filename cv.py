import smtplib
from email.message import EmailMessage
from flask_opencv_streamer.streamer import Streamer
import imghdr
import cv2
import os

port = 3030
require_login = False
streamer = Streamer(port, require_login)

snapshotLimiter = 10

password = os.getenv('PASS')

msg = EmailMessage()
msg['Subject'] = "Person detected"
msg['From'] = "bjmoffet85@gmail.com"
msg['To'] = 'teaqllabs@gmail.com'
msg.set_content("Someone has been detected at: Back door.")

cap = cv2.VideoCapture(0)
faceCas = cv2.CascadeClassifier('/home/ian/Crypt/ComputerVision/face.xml')

while True:
    ret, frame = cap.read()

    faces = faceCas.detectMultiScale(frame, 1.1, 4)

    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    try:
        if faces.any() and snapshotLimiter >= 10:
            filename = "KC_Snapshot_1.jpg"
            cv2.imwrite(filename=filename, img=frame)

            with open('KC_Snapshot_1.jpg', 'rb') as f:
                file_data = f.read()
                file_type = imghdr.what(f.name)
                file_name = f.name

                msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login("bjmoffett85@gmail.com", password)
                    smtp.send_message(msg)

                    os.system("rm KC_Snapshot_1.jpg")
                    snapshotLimiter = 1

    except AttributeError:
        pass

    if snapshotLimiter < 10:
        snapshotLimiter += .1

    print(snapshotLimiter)

    if not streamer.is_streaming:
        streamer.start_streaming()

    streamer.update_frame(frame)

    cv2.waitKey(1)
