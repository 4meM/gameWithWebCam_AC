
import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
from directkeys import A, D, Space, ReleaseKey, PressKey

class ColorDetector:
    def __init__(self):
        self.cam = VideoStream(src=0).start()
        self.currentKey = list()
        self.colourLower = np.array([20, 100, 100])
        self.colourUpper = np.array([30, 255, 255])

    def process_frame(self):
        key = False

        img = self.cam.read()
        img = np.flip(img, axis=1)
        img = np.array(img)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blurred = cv2.GaussianBlur(hsv, (11, 11), 0)

        mask = cv2.inRange(blurred, self.colourLower, self.colourUpper)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

        width = img.shape[1]
        height = img.shape[0]

        upContour = mask[0:height//2, 0:width]
        downContour = mask[3*height//4:height, 2*width//5:3*width//5]

        cnts_up = cv2.findContours(upContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_up = imutils.grab_contours(cnts_up)

        cnts_down = cv2.findContours(downContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_down = imutils.grab_contours(cnts_down)

        if len(cnts_up) > 0:
            c = max(cnts_up, key=cv2.contourArea)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                if cX < (width // 2 - 35):
                    PressKey(A)
                    key = True
                    self.currentKey.append(A)
            
                elif cX > (width // 2 + 35):
                    PressKey(D)
                    key = True
                    self.currentKey.append(D)
        
        if len(cnts_down) > 0:
            PressKey(Space)
            key = True
            self.currentKey.append(Space)

        img = cv2.rectangle(img, (0, 0), (width//2-35, height//2), (0, 255, 0), 1)
        cv2.putText(img, 'LEFT', (110, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        img = cv2.rectangle(img, (width//2+35, 0), (width, height//2), (0, 255, 0), 1)
        cv2.putText(img, 'RIGHT', (440, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        img = cv2.rectangle(img, (2*(width//5), 3*height//4), (3*width//5, height), (0, 255, 0), 1)
        cv2.putText(img, 'SET', (2*(width//5) + 20, height-10), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        cv2.imshow("Steering", img)

        if not key and len(self.currentKey) != 0:
            for current in self.currentKey:
                ReleaseKey(current)
            self.currentKey = []

        return img

    def stop(self):
        cv2.destroyAllWindows()
        self.cam.stop()