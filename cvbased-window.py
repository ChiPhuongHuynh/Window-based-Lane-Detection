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
    return mask

def threshold(frame, mask):
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

def midlane_coordinates(frame):
    histogram = np.sum(frame[frame.shape[0]//2,:], axis =0)
    midpoint = int(histogram.shape[0]/2)
    left_x = np.argmax(histogram[:midpoint])
    right_x = np.argmax(histogram[midpoint:]) + midpoint
    return (left_x + right_x) / 2
def pipeline(filename):
    img = cv2.imread(filename)
    frame = cv2.resize(img, (640,480))
    frame = transformed_frame(frame)
    mask = masking(frame)
    frame = threshold(frame,mask)
    mid = midlane_coordinates(frame)
    return mid

def main():
    filename = "nonperturbed1.png"

    mid = pipeline(filename)
    print(mid)
    
    """
    cv2.imshow('frame',frame)
    cv2.waitKey(0)"""
main()

