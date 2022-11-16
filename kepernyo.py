import cv2
import numpy as np
import mediapipe as mp
import time
import pyautogui
pyautogui.FAILSAFE = False


cap = cv2.VideoCapture(0)
camszelesseg = 640
cammagassag  = 480
cap.set(3, camszelesseg)
cap.set(4, cammagassag)
frameR = 100
run = True
x = 0
pTime = 0

mpHands = mp.solutions.hands
hands = mpHands.Hands(False,1)
mpDraw = mp.solutions.drawing_utils
tipIds = [4,8,12,16,20]
success, img = cap.read()
h, w, c = img.shape
zold = (0, 255, 0)
lila = (255,0,255)
szelesseg, magassag = pyautogui.size()

while run:
    success, img = cap.read()
    imageRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    hand_landmarks = results.multi_hand_landmarks
    if hand_landmarks:
        for handLMs in hand_landmarks:
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            for lm in handLMs.landmark:
                x, y = int(lm.x * w), int(lm.y * h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), zold, 2)
            mpDraw.draw_landmarks(img, handLMs, mpHands.HAND_CONNECTIONS)

        lista = []
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lista.append([id,cx,cy])
            x1, y1 = lista[8][1:]
            x2, y2 = lista[12][1:]
                #if id == 8 :
                    #
                    # cv2.circle(img, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            #print(x1,y1,x2,y2)


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

            if ujjak[1] == 1 and ujjak[2] == 0:

                cv2.rectangle(img, (frameR, frameR),(camszelesseg-frameR, cammagassag-frameR), lila,2)
                convertersz  = np.interp(x1,(frameR,camszelesseg-frameR),(0,szelesseg))
                convertermag = np.interp(x1,(frameR,cammagassag-frameR),(0,magassag))

                a = szelesseg - convertersz
                b = magassag  - convertermag
                pyautogui.moveTo(a,b)
                #cv2.circle(img, (int(a),int(b)), 15, zold, cv2.FILLED)
                cv2.circle(img,(x1,y1), 15, lila,cv2.FILLED)
                #mouse.move(a,convertermag)

            #if ujjak[1] == 1 and ujjak[2] == 1:
                

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Kep", img)
    cv2.waitKey(1)

