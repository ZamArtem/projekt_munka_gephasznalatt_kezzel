import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui


cap = cv2.VideoCapture(0)
camszelesseg = 640
cammagassag  = 480
cap.set(3, camszelesseg)
cap.set(4, cammagassag)
pTime = 0

lila = (255,0,255)

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1)
mpDraw = mp.solutions.drawing_utils
success, img = cap.read()
h, w, c = img.shape
run = True


while run:
    success, img = cap.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
                mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)
        
        lista = []
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lista.append([id,cx,cy])

                if id == 8 :
                    print(cx,cy)
                    cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        cv2.rectangle(img,(100,100),(camszelesseg-100, cammagassag-100), lila,2)






    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Kep", img)
    cv2.waitKey(1)
