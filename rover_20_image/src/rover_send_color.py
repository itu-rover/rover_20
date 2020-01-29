#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import numpy as np

image_pub = rospy.Publisher("image_topic",Image,queue_size=1)
bridge = CvBridge()
bridge.frame_id="camera_link"
rospy.init_node('image_converter', anonymous=True)
camera= cv2.VideoCapture(0)

bLow  = 0
bHigh = 16
gLow  = 0
gHigh = 255
rLow  = 54
rHigh = 255

while not rospy.is_shutdown():
    ret, frame=camera.read()
    rgbLow=np.array([bLow,gLow,rLow])
    rgbHigh=np.array([bHigh,gHigh,rHigh])
    maskedImage = cv2.inRange(frame, rgbLow, rgbHigh)
    # cv2.imshow('Masked Image', maskedImage)
    frame  =  cv2.resize(frame, (300, 300))
    kernel = np.ones((2,2),np.uint8)
    # the first morphological transformation is called opening, it will sweep out extra lone pixels around the image
    openedImage = cv2.morphologyEx(maskedImage, cv2.MORPH_OPEN, kernel)
    # cv2.imshow("Open Image", openedImage)
    # Invert the black and white parts of the image for our next algorithm
    invertedImage = cv2.bitwise_not(openedImage)
    # cv2.imshow("Inverted Image", invertedImage)
    # Let's implement some nice algorithm called blob detection to detect the cube
    # https://www.learnopencv.com/blob-detection-using-opencv-python-c/
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 200
     
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.3
    params.maxCircularity = 1
     
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87
     
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.5

    # Apply the detector
    detector = cv2.SimpleBlobDetector_create(params)
    # Extract keypoints
    keypoints = detector.detect(invertedImage)
    # Apply to the Image 
    outputImage = cv2.drawKeypoints(frame, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("Output Image", outputImage)

    # A variable to carry the number of keypoints in the loop
    keypointCounter = 0
    # Variables to hold x and y coordinates of the keypoints
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    # Iterate and extract the positions and size of each keypoint detected
    for keypoint in keypoints:
        # Get x andy coordinates and sizes of the keypoints
        x = keypoint.pt[0]
        y = keypoint.pt[1]
        s = keypoint.size
        
        s = s/2
        x1.append((int)(x-s))
        y1.append((int)(y-s))
        x2.append((int)(x+s))
        y2.append((int)(y+s))
        # Draw bounding box
        cv2.rectangle(outputImage,(x1[keypointCounter],y1[keypointCounter]),(x2[keypointCounter],y2[keypointCounter]), (0,255,0),2)
        keypointCounter = keypointCounter + 1

    # show Bboxed Image
    # cv2.imshow("Bboxed Image", outputImage)
    image_pub.publish(bridge.cv2_to_imgmsg(outputImage, "bgr8"))

camera.release()
cv2.destroyAllWindows()
