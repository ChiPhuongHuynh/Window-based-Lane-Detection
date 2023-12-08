import cv2
import numpy as np
import sys

def nothing(x):
    pass

def transformed_frame(frame):
    lower_right = (625, 396)
    upper_right = (427, 288)
    lower_left = (14,394)
    upper_left = (215,284)

    src = np.float32([upper_left, lower_left, upper_right, lower_right])
    dst = np.float32([[0, 0], [0, 480], [640, 0], [640, 480]])

    matrix = cv2.getPerspectiveTransform(src, dst)
    transformed_frame = cv2.warpPerspective(frame, matrix, (640,480))
    return transformed_frame

def masking(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l = np.array([0,0,200])
    u = np.array([255,50,255])

    mask = cv2.inRange(hsv, l, u)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

def main():
    #filename = sys.argv[1]
    filename = "nonperturbed1.png"
    img = cv2.imread(filename)
    frame = cv2.resize(img, (640,480))
    frame = transformed_frame(frame)
    frame = masking(frame)
    cv2.imshow('frame',frame)
    cv2.waitKey(0)
main()