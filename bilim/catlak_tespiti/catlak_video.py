import cv2
import numpy as np
from matplotlib import pyplot as plt


camera=cv2.VideoCapture(0)
camera.set(3,720)
camera.set(4,405)

while (1):
    ret,frame=camera.read()

    #Converting Gray
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #masking

    gaus=cv2.GaussianBlur(gray,(5,5),3)
    mask=cv2.erode(gaus,None,iterations=3)
    mask=cv2.dilate(mask,None,iterations=2)
    laplacian = cv2.Laplacian(frame, cv2.CV_64F)
    sobel_horizontal = cv2.Sobel(frame, cv2.CV_64F, 1, 0, ksize=5)
    sobel_vertical = cv2.Sobel(frame, cv2.CV_64F, 0, 1, ksize=5)
    median=cv2.medianBlur(frame,5,2)
    #canny edge

    canny=cv2.Canny(mask,40,50)
    cv2.imshow('sobel_vertical',sobel_vertical)
    cv2.imshow('Mask',mask)
    cv2.imshow('Laplacian',laplacian)
    cv2.imshow('frame',frame)
    cv2.imshow('Sobel',sobel_horizontal)
    cv2.imshow('canny',canny)
    cv2.imshow('Median',median)
    cv2.imshow("Gaussian",gaus)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()