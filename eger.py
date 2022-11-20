import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui
import math
pyautogui.FAILSAFE = False

"""
import pygame
from mss import mss
from PIL import Image
"""


cap = cv2.VideoCapture(0)
camsz = 640
camm  = 480
cap.set(3, camsz)
cap.set(4, camm)
pTime = 0

lila = (255,0,255)

sz, m = pyautogui.size()
x = sz / 640
y = m / 480


mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1)
mpDraw = mp.solutions.drawing_utils
success, img = cap.read()
h, w, c = img.shape
run = True
tipIds = [4,8,12,16,20]

while run:
    success, img = cap.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
                mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)
        
        #lista = []
        lista = []
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lista.append([id,cx,cy])
            x1, y1 = lista[8][1:]
            x2, y2 = lista[12][1:]


            ujjak = []

            if lista[tipIds[0]][1] > lista[tipIds[0] - 1][1]:
                ujjak.append(1)
            else:
                ujjak.append(0)
            for id in range(1,5):
                if lista[tipIds[id]][2] < lista[tipIds[id] - 2][2]:
                    ujjak.append(1)
                else:
                    ujjak.append(0)
                
            if id == 8 :
                print(cx, cy, "a")
                szel = (cx - 100) * x
                mag =  (cy) * y
                print(szel, mag)

                pyautogui.moveTo(int(szel), int(mag))
                cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
        cv2.rectangle(img,(100,100),(camsz-100, camm-100), lila,2)




 

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Kep", img)
    cv2.waitKey(1)
