#!/usr/bin/env python
import numpy as np
import imutils
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import rosparam
from cv_bridge import CvBridge, CvBridgeError

cv_imageMsg = Image()

greenLower = (29, 86, 6)#29,86,6
greenUpper = (64, 255, 255)
imageTopic = rospy.get_param('RoverReachImage/ImageProcessing/sub_image','/zed/left/image_rect_color')
pxTopic = rospy.get_param('RoverReachImage/ImageProcessing/pub_pxCoordinates','/px_coordinates')
bridge = CvBridge()

def imageCallback(data):

	frame = bridge.imgmsg_to_cv2(data, "bgr8")

	(rows,cols,channels) = frame.shape
	if cols > 60 and rows > 60:
		cv2.circle(frame, (50,50), 10, 255)

	#frame = imutils.resize(frame, width=1200)
	#frame = cv2.GaussianBlur(frame, (11, 11), 0)
	#Blur eklenmeli eklenmeli mi hala emin degilim
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=3)
	mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None
		
		# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		#print("Center x:{0} and y:{1}\n ".format(x,y))
		# only proceed if the radius meets a minimum size
		if radius > 0.5:
			# draw the circle and centroid on the frame,
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

			frameHeight = frame.shape[0]
			frameWidth = frame.shape[1]
			coordinatePublisher.publish(str(x) +","+ str(y) + "," + str(frameWidth) + "," + str(frameHeight))
	else:

		coordinatePublisher.publish("-")

			


	cv2.imshow("Frame", frame)
	cv2.waitKey(1)
	

def main():
	global cv_imageMsg
	


if __name__ == '__main__':

	try:
		rospy.init_node('rover_detect_video')		
		coordinatePublisher = rospy.Publisher(pxTopic,String,queue_size = 100)
		rospy.Subscriber(imageTopic, Image, imageCallback)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass
