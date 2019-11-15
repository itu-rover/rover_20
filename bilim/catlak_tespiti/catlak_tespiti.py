#!/usr/bin/env python

import cv2
import numpy as np


img=cv2.imread('urc_science1.png')
img_counter=0



cv2.resize(img,(144,144))
#Converting Gray
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

#masking

mask=cv2.GaussianBlur(gray,(5,5),3)
mask=cv2.erode(mask,None,iterations=3)
mask=cv2.dilate(mask,None,iterations=2)

#canny edge

canny=cv2.Canny(mask,20,40) #80 100 #20 #40
laplacian = cv2.Laplacian(img, cv2.CV_64F)
sobel_horizontal = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobel_vertical = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)
median=cv2.medianBlur(img,5,2)



#cv2.imshow('Laplacian',laplacian)
cv2.imshow('normal',img)
#cv2.imshow('Sobel',sobel_horizontal)
cv2.imshow('canny',canny)
#cv2.imshow('Median',median)
#cv2.imshow('canny',canny)



img_name = "crack_urc_science{}.png".format(img_counter)
cv2.imwrite(img_name, canny)
print("{} written!".format(img_name))

cv2.waitKey(0)
cv2.destroyAllWindows()
