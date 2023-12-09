import cv2
import numpy as np
import sys

def nothing(x):
    pass

"""
Does bird eye transformation on an image sized 640x480
Input: a cv.open image
Output: bird's eye view image
"""
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


"""
Apply custom HSV color masking to the image
Input: a cv.open image
Output: color mask
"""
def masking(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    l = np.array([0,0,200])
    u = np.array([255,50,255])
    mask = cv2.inRange(hsv, l, u)
    return mask

"""
Apply thresholding to the image
Input: cv.open image and a color mask
Output: Black background and white lane image
"""
def threshold(frame, mask):
    result = cv2.bitwise_and(frame, frame, mask=mask)
    return result

"""
Does histogram based lane coordinate calculation
Input: cv.open image
Output: values of middle lane line
"""
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
        print(left_x)
        print(right_x)
        return (left_x + right_x) / 2

    return -1
"""
Generate mid lane lines for visualization
Input: cv.open image and middle line x-coordinate
Output: image with middle lane drawn 
"""
def midlane_draw(frame, mid):
    cv2.line(frame,(int(mid-50),0),(int(mid-50),640),(255,0,0),5)
    cv2.line(frame, (int(mid+50),0),(int(mid+50),640),(255,0,0),5)
    return frame
"""
Applies detection as a pipeline
"""
def pipeline(filename):
    #filename = "nonperturbed1.png"
    img = cv2.imread(filename)
    frame = cv2.resize(img, (640,480))
    frame = transformed_frame(frame)
    mask = masking(frame)
    frame = threshold(frame,mask)
    mid = midlane_coordinates(frame)
    return mid

def main():
    filename = "nonperturbed1.png"
    img = cv2.imread(filename)
    img = cv2.resize(img, (640,480))
    tf = transformed_frame(img)
    mask = masking(tf)
    frame = threshold(tf,mask)


    mid = pipeline(filename)
    frame= midlane_draw(frame, mid)
    cv2.imshow('original',img)
    cv2.imshow('transformed_frame',tf)
    cv2.imshow('Mask',mask)
    cv2.imshow('Midlane Outline',frame)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

main()
