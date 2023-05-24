import cv2
import mediapipe as mp
from HandTrackingModule import handDetector
import time

numdict = {0:"Wrist", 1:"Thumb_CMC", 2:"Thumb_MCP", 3:"Thumb_IP", 4:"Thumb_TIP",
           5:"Index_MCP", 6:"Index_PIP", 7:"Index_DIP", 8:"Index_TIP", 9:"Middle_MCP",
           10:"Middle_PIP", 11:"Middle_DIP", 12:"Middle_TIP", 13:"Ring_MCP", 14:"Ring_PIP",
           15:"Ring_DIP", 16:"Ring_TIP", 17:"Pinky_MCP", 18:"Pinky_PIP", 19:"Pinky_DIP",
           20:"Pinky_TIP"}
print(numdict)
num = int(input("Number:"))
    
if 0 <= num < 21:
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        PosList = detector.findPosition(img, num)

        if len(PosList) != 0:
            print("Number "+str(num)+" ("+str(numdict[num])+") Position is: "+str(PosList[num][1:]))

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        
        cv2.putText(img, ("fps:"+str(int(fps))), (5,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0),2)
        cv2.imshow("image",img)
        key = cv2.waitKey(1) & 0xFF
        if key==ord('q'):
            break
else:
    print("Wrong number, try again!!")