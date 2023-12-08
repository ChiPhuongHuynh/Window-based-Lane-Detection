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
    histogram = np.sum(frame[240:, :], axis =0)
    midpoint = int(histogram.shape[0]/2)
    #print(histogram.shape)
    #print(midpoint)
    left_x = np.argmax(histogram[:midpoint,2])
    #print(left_x)
    right_x = np.argmax(histogram[midpoint:,2]) + midpoint
    #print(right_x)

    mid_value = (histogram[left_x,2] + histogram[right_x,2]) / 2
    if (mid_value > 20000):
        return (left_x + right_x) / 2

    return -1

def pipeline(filename):
    #filename = "nonperturbed1.png"
    img = cv2.imread(filename)
    frame = cv2.resize(img, (640,480))
    frame = transformed_frame(frame)
    mask = masking(frame)
    frame = threshold(frame,mask)
    mid = midlane_coordinates(frame)
    return mid

def sliding_window(frame, left_l, right_l):
    #contours is the shifting of white pixels
    lx = []
    rx = []
    y = 479

    while y > 0:
        img = frame[y-40:y, left_l-50:left_l+50]
        contours,h = cv2.findContours(img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            m = cv2.moments(c)
            if(m["m00"] != 0):
                cx = int(m["m10"] / m["m01"]) #center of the contours
                left_l = left_l - 50 + cx
                lx.append(left_l)

        img = frame[y-40:y, right_l-50:right_l+50]
        contours,h = cv2.findContours(img, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            m = cv2.moments(c)
            if(m["m00"] != 0):
                cx = int(m["m10"] / m["m00"]) #center of the contours
                right_l = right_l - 50 + cx
                rx.append(right_l)
        midx = int((right_l+left_l)/2)

        cv2.rectangle(frame, (midx-25,y), (midx+25,y-40), (255,255,255), 1)
        y = y - 40
    return frame

def midlane_draw(frame, mid):
    img = np.zeros((512,512,3), np.uint8)
    cv2.line(img,(0,0),(511,511),(255,0,0),5)
    frame = img
    return frame

def main():
    filename = "nonperturbed1.png"

    img = cv2.imread(filename)
    frame = cv2.resize(img, (640,480))

    mid = pipeline(filename)

    """
    cv2.imshow('contours',frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()"""

main()
