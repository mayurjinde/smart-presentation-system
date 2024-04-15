import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np
import pyautogui

# Parameters
width, height = 1280, 720
gestureThreshold = 400
folderPath = "presentation"
pTime = 0
cTime = 0

# Camera Setup
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS,60)
# fpsReader = cvzone.FPS()
# cap.set(3, width)
# cap.set(4, height)
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)
# Variables
# imgList = []
# delay = 10
# buttonPressed = False
# counter = 0
# drawMode = False
# imgNumber = 0
# delayCounter = 0
# annotations = [[]]
# annotationNumber = -1
# annotationStart = False
# hs, ws = int(120 * 1), int(213 * 1)  # width and height of small image
# # Get list of presentation images
# pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)


# faceDetect=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

class Video(object):
    def __init__(self):
        self.cap=cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS,60)
        self.fpsReader = cvzone.FPS()
        self.cap.set(3, width)
        self.cap.set(4, height)
        self.imgNumber = 0
        self.imgList = []
        self.delay = 20
        self.buttonPressed = False
        self.counter = 0
        self.drawMode = False
        self.imgNumber = 0
        self.delayCounter = 0
        self.annotations = [[]]
        self.annotationNumber = -1
        self.annotationStart = False
        self.hs, self.ws = int(120 * 1), int(213 * 1)  # width and height of small image
        # Get list of presentation images
        self.pathImages = sorted(os.listdir(folderPath), key=len)
        print(self.pathImages)
    def __del__(self):
        self.cap.release()
    def get_frame(self):
        # ret,frame=self.video.read()
        # faces=faceDetect.detectMultiScale(frame, 1.3, 5)
        # for x,y,w,h in faces:
        #     x1,y1=x+w, y+h
        #     cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,255), 1)
        #     cv2.line(frame, (x,y), (x+30, y),(255,0,255), 6) #Top Left
        #     cv2.line(frame, (x,y), (x, y+30),(255,0,255), 6)

        #     cv2.line(frame, (x1,y), (x1-30, y),(255,0,255), 6) #Top Right
        #     cv2.line(frame, (x1,y), (x1, y+30),(255,0,255), 6)

        #     cv2.line(frame, (x,y1), (x+30, y1),(255,0,255), 6) #Bottom Left
        #     cv2.line(frame, (x,y1), (x, y1-30),(255,0,255), 6)

        #     cv2.line(frame, (x1,y1), (x1-30, y1),(255,0,255), 6) #Bottom right
        #     cv2.line(frame, (x1,y1), (x1, y1-30),(255,0,255), 6)
        success, img = self.cap.read()
        img = cv2.flip(img, 1)
        pathFullImage = os.path.join(folderPath, self.pathImages[self.imgNumber])
        imgCurrent = cv2.imread(pathFullImage)
        # Find the hand and its landmarks
        hands, img = detectorHand.findHands(img)

        # Draw Gesture Threshold line
        cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 10)
        if hands and self.buttonPressed is False:  # If hand is detected
            hand = hands[0]
            cx, cy = hand["center"]
            lmList = hand["lmList"]  # List of 21 Landmark points
            fingers = detectorHand.fingersUp(hand)  # List of which fingers are up
            # Constrain values for easier drawing
            xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
            yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
            indexFinger = xVal, yVal
            if cy <= gestureThreshold:  # If hand is at the height of the face
                if fingers == [1, 0, 0, 0, 0]:
                    print("Left")
                    self.buttonPressed = True
                    if self.imgNumber > 0:
                        self.imgNumber -= 1
                        self.annotations = [[]]
                        self.annotationNumber = -1
                        self.annotationStart = False
                if fingers == [0, 0, 0, 0, 1]:
                    print("Right")
                    self.buttonPressed = True  
                    if self.imgNumber < len(self.pathImages) - 1:
                        self.imgNumber += 1
                        self.annotations = [[]]
                        self.annotationNumber = -1
                        self.annotationStart = False    
            if fingers == [0, 1, 1, 0, 0]:
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)  
            # if fingers == [0, 1, 0, 0, 1]:
            #     pyautogui.press('f11')
            if fingers == [0, 1, 0, 0, 0]:
                if self.annotationStart is False:
                    self.annotationStart = True
                    self.annotationNumber += 1
                    self.annotations.append([])
                print(self.annotationNumber)
                self.annotations[self.annotationNumber].append(indexFinger)
                cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)   
            else:
                self.annotationStart = False     
            if fingers == [0, 1, 1, 1, 0]:
                if self.annotations:   
                    self.annotations.pop(-1)
                    self.annotationNumber -= 1
                    self.buttonPressed = True 

        else:
            self.annotationStart = False 
        if self.buttonPressed:
            self.counter += 1
            if self.counter > self.delay:
                self.counter = 0
                self.buttonPressed = False
        for i, self.annotation in enumerate(self.annotations):
            for j in range(len(self.annotation)):
                if j != 0:
                    cv2.line(imgCurrent, self.annotation[j - 1], self.annotation[j], (0, 0, 200), 12)

        imgSmall = cv2.resize(img, (self.ws, self.hs))
        h, w, _ = imgCurrent.shape
        h1 , w1, l1 = img.shape  
        imgCurrent[0:self.hs, w - self.ws: w] = imgSmall 
        fps , imgCurrent = self.fpsReader.update(imgCurrent)         







        ret,jpg=cv2.imencode('.jpg',imgCurrent)
        return jpg.tobytes()