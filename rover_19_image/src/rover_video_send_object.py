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
kamera = cv2.VideoCapture(0)
kamera.set(cv2.CAP_PROP_FPS, 30)
indicator_red_cascade = cv2.CascadeClassifier('indicator-red.xml')
indicator_green_cascade = cv2.CascadeClassifier('indicator-green.xml')
indicator_white_cascade = cv2.CascadeClassifier('indicator-white.xml')
two_state_lever_switch_cascade = cv2.CascadeClassifier('2-state-lever-switch.xml')
socket_cascade = cv2.CascadeClassifier('socket.xml')
two_state_rot_main_switch_cascade = cv2.CascadeClassifier('2-state-rot-main-switch.xml')
two_state_rot_switch_cascade = cv2.CascadeClassifier('2-state-rot-switch.xml')
press_button_cascade = cv2.CascadeClassifier('press-button.xml')
pipe_cascade = cv2.CascadeClassifier('pipe.xml')
font = cv2.FONT_HERSHEY_SIMPLEX
def color_detect(bl, bh, gl, gh, rl, rh, frame, type):
    rgbLow = np.array([bl, gl, rl])
    detected = 0
    a = 0
    b = 0
    c = 0
    d = 0
    rgbHigh = np.array([bh, gh, rh])
    maskedImage = cv2.inRange(frame, rgbLow, rgbHigh)
    string = "Masked Image" + str(type)
    cv2.imshow(string, maskedImage)
    kernel = np.ones((2, 2), np.uint8)
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
    # outputImage = cv2.drawKeypoints(frame, keypoints, np.array([]), (0, 0, 255),
    #                           cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
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

        s = s / 2
        x1.append((int)(x - s))
        y1.append((int)(y - s))
        x2.append((int)(x + s))
        y2.append((int)(y + s))
        detected = 1
        a = x1[keypointCounter]
        b = y1[keypointCounter]
        c = x2[keypointCounter]
        d = y2[keypointCounter]
        keypointCounter = keypointCounter + 1
        # Draw bounding box
        # cv2.rectangle(outputImage, (x1[keypointCounter], y1[keypointCounter]),
        #        (x2[keypointCounter], y2[keypointCounter]), (0, 255, 0), 2)

    return (detected, a, b, c, d)


while not rospy.is_shutdown():


    a = []
    b = []
    c = []
    d = []

    detected = []
    i = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    for l in i:
        detected.append(l)
        a.append(l)
        b.append(l)
        c.append(l)
        d.append(l)
        ret, frame = kamera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        red = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # green=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
        # blue=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        lower_rgb_red = np.array([0, 0, 117])
        upper_rgb_red = np.array([38, 255, 255])
        mask_red = cv2.inRange(red, lower_rgb_red, upper_rgb_red)

        indicator_red = indicator_red_cascade.detectMultiScale(gray, 1.3, 4)
        indicator_green = indicator_green_cascade.detectMultiScale(gray, 1.3, 4)
        indicator_white = indicator_white_cascade.detectMultiScale(gray, 1.3, 4)
        socket = socket_cascade.detectMultiScale(gray, 1.3, 4)
        two_state_rot_main_switch = two_state_rot_main_switch_cascade.detectMultiScale(gray, 1.3, 4)
        two_state_lever_switch = two_state_lever_switch_cascade.detectMultiScale(gray, 1.3, 4)
        two_state_rot_switch = two_state_rot_switch_cascade.detectMultiScale(gray, 1.3, 4)
        pipe = pipe_cascade.detectMultiScale(gray, 1.3, 4)
        # three_state_rot_switch = three_state_rot_switch_cascade.detectMultiScale(gray, 1.3, 4)
        press_button = press_button_cascade.detectMultiScale(gray, 1.3, 4)

        detected[0] = 0
        detected[1] = 0

        # detected[2], a[2], b[2], c[2], d[2] = color_detect(189, 255, 0, 208, 58, 210, frame, 2)  # for white

        for (x, y, w, h) in socket:
            detected[3], a[3], b[3], c[3], d[3] = color_detect(61, 145, 0, 77, 54, 125, frame, 3)  # for socket
            if (detected[3]):
                cv2.rectangle(frame, (x, y), (w + x, h + y), (0, 255, 255), 2)
                cv2.putText(frame, 'socket', (x - 2, y - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        for (x, y, w, h) in two_state_lever_switch:
            cv2.rectangle(frame, (x, y), (w + x, h + y), (0, 255, 255), 2)
            cv2.putText(frame, ' two_state_lever_switch', (x - 2, y - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        '''
        for (x, y, w, h) in two_state_rot_main_switch1
            detected[0], a[0], b[0], c[0], d[0] = color_detect(23, 124, 0, 98, 129, 221, frame, 0)  # for red
            if (detected[0]):
                cv2.rectangle(frame, (x, y), (w + x, h + y), (0, 255, 255), 2)
                cv2.putText(frame, ' two_state_rot_main_switch', (x - 2, y - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        for (x, y, w, h) in two_state_rot_switch:
            detected[3], a[3], b[3], c[3], d[3] = color_detect(61, 145, 0, 77, 54, 125, frame, 3)  # for socket
            if (detected[3]):
                cv2.rectangle(frame, (x, y), (w + x, h + y), (0, 255, 255), 2)
                cv2.putText(frame, ' two_state_rot_switch', (x - 2, y - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        '''
        for (x, y, w, h) in indicator_red:
            detected[0], a[0], b[0], c[0], d[0] = color_detect(23, 124, 0, 98, 129, 221, frame, 0)  # for red
            if (detected[0]):
                cv2.rectangle(frame, (a[0], b[0]), (c[0], d[0]), (0, 255, 255), 2)
                cv2.putText(frame, 'indicator_red', (a[0] - 2, b[0] - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

        for (x, y, w, h) in indicator_green:
            detected[1], a[1], b[1], c[1], d[1] = color_detect(103, 138, 105, 255, 56, 95, frame, 1)  # for green
            if (detected[1]):
                cv2.rectangle(frame, (a[1], b[1]), (c[1], d[1]), (0, 255, 255), 2)
                cv2.putText(frame, 'indicator_green', (a[1] - 2, b[1] - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        '''
        for (x, y, w, h) in pipe:

            detected[4], a[4], b[4], c[4], d[4] = color_detect(0, 255, 66, 255, 0, 67, frame, 4)  # for pipe
            print(detected[4])
            if (detected[4]):
                cv2.rectangle(frame, (a[1], b[1]), (c[1], d[1]), (0, 255, 255), 2)
                cv2.putText(frame, 'pipe', (a[1] - 2, b[1] - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        
        for (x, y, w, h) in press_button:
            detected[1], a[1], b[1], c[1], d[1] = color_detect(103, 138, 105, 255, 56, 95, frame, 1)  # for green
            if (detected[1]):
                cv2.rectangle(frame, (x, y), (w + x, h + y), (0, 255, 255), 2)
                cv2.putText(frame, ' press-button', (x - 2, y - 2), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
        '''
        image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
kamera.release()
cv2.destroyAllWindows()

