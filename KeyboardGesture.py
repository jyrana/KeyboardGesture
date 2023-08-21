import cv2
import time
import numpy as np
import handtracking2 as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
wCam,hCam = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
pTime =0
ditector = ht.handDitector(detectionCon = 0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar =0
per = 0
bri = 0
while True:
    success,img = cap.read()
    img = ditector.findHands(img)
    lmlist = ditector.findPosition(img,draw = False)
    if len(lmlist)!=0:
        #print(lmlist[4],lmlist[8])
        x1,y1 = lmlist[4][1],lmlist[4][2]
        x2,y2 = lmlist[8][1],lmlist[8][2]
        x3,y3 = lmlist[20][1],lmlist[20][2]



        cx,cy = (x1+x2)//2 , (y1+y2)//2
        cv2.circle(img,(x1,y1),15,(255,0,0),cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),2)
        cv2.circle(img, (cx, cy), 15, (255, 0, 0), cv2.FILLED)
        length = np.math.hypot(x2 - x1, y2 - y1)
        lengthbri = np.math.hypot(x3-x1,y3-y1)
        #print(length)
        vol = np.interp(length,[30,230],[minVol,maxVol])
        volBar = np.interp(length, [30, 230], [300, 100])
        per = np.interp(length, [30, 230], [0, 100])
        bri = np.interp(lengthbri, [50, 300], [10, 100])
        #print(vol)
        volume.SetMasterVolumeLevel(vol, None)
        #sbc.fade_brightness(bri)
        if length <30:
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        cv2.rectangle(img,(50,100),(85,300),(255,0,255),3)
        cv2.rectangle(img, (50, int(volBar)), (85, 300), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (50, 350), cv2.FONT_HERSHEY_PLAIN, 2, (255,0, 255), 3)
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime =cTime
    cv2.putText(img,f'FPS:{int(fps)}',(40,50),cv2.FONT_HERSHEY_PLAIN,2,(0,255,255),3)
    cv2.imshow("img",img)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break