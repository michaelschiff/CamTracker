import cv2 as cv
import numpy as np

class Helper():
    def __init__(self):
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.dragging = False
        self.ROI = None
        self.ROI_HSV_HIST = None

def callback(event, x, y, flags, params):
    helper = params[0]
    img = params[1]
    if (event == cv.cv.CV_EVENT_LBUTTONDOWN):
        helper.x1 = x
        helper.x2 = x
        helper.y1 = y
        helper.y2 = y
        helper.dragging = True
    if (event == cv.cv.CV_EVENT_LBUTTONUP):
        helper.x2 = x
        helper.y2 = y
        helper.dragging = False
        helper.ROI = img[helper.y1+1:helper.y2, helper.x1+1:helper.x2]
        helper.ROI = cv.GaussianBlur(helper.ROI, (15,15), 0)
        #helper.ROI = cv.cvtColor(helper.ROI, cv.cv.CV_BGR2HSV)
    if (event == cv.cv.CV_EVENT_MOUSEMOVE):
        if (helper.dragging):
            helper.x2 = x
            helper.y2 = y

cv.namedWindow("main")
cv.namedWindow("ROI")
capture = cv.VideoCapture(0)
helper = Helper()
parameters = [helper, None]
cv.setMouseCallback("main", callback, parameters)
while True:
    succ, frame = capture.read()
    frame = cv.flip(frame, 1)
    parameters[1] = frame
    if helper.dragging:
        cv.rectangle(frame, (helper.x1, helper.y1), (helper.x2, helper.y2), (255, 0, 0))
    if (helper.ROI is not None):
        cv.imshow("ROI", helper.ROI)
        match = cv.matchTemplate(frame, helper.ROI, cv.cv.CV_TM_CCORR)
        cv.imshow("match", match)
    cv.imshow("main", frame)
    x = cv.waitKey(1)
    if x == 113: break
cv.destroyAllWindows()
