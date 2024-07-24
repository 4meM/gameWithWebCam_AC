import cv2
import imutils
from imutils.video import VideoStream
import numpy as np
from directkeys import A, D, W, S, ReleaseKey, PressKey
import time

class ColorDetector:
    def __init__(self):
        self.cam = VideoStream(src=0).start()
        self.currentKey = []
        self.colourLower = np.array([20, 100, 100])
        self.colourUpper = np.array([30, 255, 255])

        self.lastPressTimes = {
            A: 0,
            D: 0,
            W: 0,
            S: 0
        }
        self.pressInterval = 0.02  # Intervalo de tiempo en segundos entre presiones de teclas

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

        # Definir los sectores con un espaciado adecuado
        upContour = mask[0:height//3, 0:width]
        downContour = mask[2*height//3:height, 0:width]
        leftContour = mask[height//3:2*height//3, 0:width//3]
        rightContour = mask[height//3:2*height//3, 2*width//3:width]

        cnts_up = cv2.findContours(upContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_up = imutils.grab_contours(cnts_up)

        cnts_down = cv2.findContours(downContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_down = imutils.grab_contours(cnts_down)

        cnts_left = cv2.findContours(leftContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_left = imutils.grab_contours(cnts_left)

        cnts_right = cv2.findContours(rightContour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts_right = imutils.grab_contours(cnts_right)

        currentTime = time.time()
        pressed_keys = []

        # Check UP
        if len(cnts_up) > 0:
            if currentTime - self.lastPressTimes[W] > self.pressInterval:
                PressKey(W)
                pressed_keys.append(W)
                self.lastPressTimes[W] = currentTime

        # Check DOWN
        if len(cnts_down) > 0:
            if currentTime - self.lastPressTimes[S] > self.pressInterval:
                PressKey(S)
                pressed_keys.append(S)
                self.lastPressTimes[S] = currentTime

        # Check LEFT
        if len(cnts_left) > 0:
            if currentTime - self.lastPressTimes[A] > self.pressInterval:
                PressKey(A)
                pressed_keys.append(A)
                self.lastPressTimes[A] = currentTime

        # Check RIGHT
        if len(cnts_right) > 0:
            if currentTime - self.lastPressTimes[D] > self.pressInterval:
                PressKey(D)
                pressed_keys.append(D)
                self.lastPressTimes[D] = currentTime

        # Release keys that are not pressed
        for key in [A, D, W, S]:
            if key not in pressed_keys:
                if key in self.currentKey:
                    ReleaseKey(key)

        # Update currentKey
        self.currentKey = pressed_keys

        # Draw rectangles
        img = cv2.rectangle(img, (0, 0), (width, height//3), (0, 255, 0), 1)
        cv2.putText(img, 'UP', (width//2 - 30, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        img = cv2.rectangle(img, (0, 2*height//3), (width, height), (0, 255, 0), 1)
        cv2.putText(img, 'DOWN', (width//2 - 40, height - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        img = cv2.rectangle(img, (0, height//3), (width//3, 2*height//3), (0, 255, 0), 1)
        cv2.putText(img, 'LEFT', (20, height//2), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        img = cv2.rectangle(img, (2*width//3, height//3), (width, 2*height//3), (0, 255, 0), 1)
        cv2.putText(img, 'RIGHT', (width - 100, height//2), cv2.FONT_HERSHEY_DUPLEX, 1, (139, 0, 0))

        # El área central no debe tener texto asociado
        img = cv2.rectangle(img, (width//3, height//3), (2*width//3, 2*height//3), (0, 255, 0), 1)

        cv2.imshow("Steering", img)

        return img

    def stop(self):
        cv2.destroyAllWindows()
        self.cam.stop()



