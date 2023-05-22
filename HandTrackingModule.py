import cv2
import mediapipe as mp
import time
numdict = {0:"Wrist", 1:"Thumb_CMC", 2:"Thumb_MCP", 3:"Thumb_IP", 4:"Thumb_TIP",
           5:"Index_MCP", 6:"Index_PIP", 7:"Index_DIP", 8:"Index_TIP", 9:"Middle_MCP",
           10:"Middle_PIP", 11:"Middle_DIP", 12:"Middle_TIP", 13:"Ring_MCP", 14:"Ring_PIP",
           15:"Ring_DIP", 16:"Ring_TIP", 17:"Pinky_MCP", 18:"Pinky_PIP", 19:"Pinky_DIP",
           20:"Pinky_TIP"}
print(numdict)
num = int(input("Number:"))

class handDetector():
    def __init__(self, mode=False, maxHands=2, modelC=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelC = modelC
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelC, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0):
        PosList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                PosList.append([id, cx, cy])
                if id == num:
                    cv2.circle(img, (cx,cy), 15, (255,0,0), 3)
        return PosList

def main(num):
    if 0 <= num < 21:
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(0)
        detector = handDetector()
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            PosList = detector.findPosition(img)

            if len(PosList) != 0:
                print("Number "+str(num)+" ("+str(numdict[num])+") Position is: "+str(PosList[num][1:]))

            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img, ("fps:"+str(int(fps))), (5,30), cv2.FONT_HERSHEY_DUPLEX, 1, (255,0,0),2)
                
            cv2.imshow("image",img)
            cv2.waitKey(1)
    else:
        print("Wrong number, try again!!")

if __name__ == "__main__":
    main(num)