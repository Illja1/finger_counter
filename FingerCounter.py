import cv2
import os
import time
import HandTrakingModule as htm

wCam,hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    ret,frame = cap.read()
    frame = detector.findHands(frame)
    lmList =detector.findPosition(frame,draw=False)


    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
       
        cv2.rectangle(frame, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(frame, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)
    
    cv2.imshow('Image',frame)
    cv2.waitKey(1)