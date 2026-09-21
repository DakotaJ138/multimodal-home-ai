import cv2
import mediapipe as mp
import numpy as np

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils

stream = cv2.VideoCapture(0)
stream.set(3, 1920)
stream.set(4,1080)


if not stream.isOpened():
    print("no stream ")
    exit()

while(stream.isOpened()):
    ret, frame = stream.read()
    if not ret:
        print("no more stream")
        break

    cv2.imshow("usb camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

stream.release()
cv2.destroyAllWindows()