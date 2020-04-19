#!/usr/bin/env python

import cv2
import numpy as np
import imutils

img=cv2.imread('urc_science1.png')
down = cv2.resize(img,(640,380))

#Converting Gray
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#masking

mask=cv2.GaussianBlur(gray,(5,5),3)
mask=cv2.erode(mask,None,iterations=3)
mask=cv2.dilate(mask,None,iterations=2)

cv2.putText(img,'Cracks are detected !!',(150,100),cv2.FONT_HERSHEY_COMPLEX,1.0, (255, 255, 255),cv2.LINE_AA)

#canny edge
canny=cv2.Canny(mask,40,50)
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
median=cv2.medianBlur(img,5,2)



cv2.imshow('Laplacian',laplacian)
cv2.imshow('normal',img)
cv2.imshow('Sobel',sobel_horizontal)
cv2.imshow('canny',canny)
cv2.imshow('Median',median)
cv2.imshow('canny',canny)


cv2.waitKey(0)
cv2.destroyAllWindows()
