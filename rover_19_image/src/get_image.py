#!/usr/bin/env python

## This is the imageMsg converter code for ITU Rover Team
import rospy
from std_msgs.msg import String
from rover_state_mach.msg import RoverStateMsg
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time
import cv2

bridge = CvBridge()

def imageCallBack(data):
	cv_image = bridge.imgmsg_to_cv2(data, "bgr8")

	(rows,cols,channels) = cv_image.shape
	if cols > 60 and rows > 60:
	  cv2.circle(cv_image, (50,50), 10, 255)

	cv2.imshow("Image window", cv_image)
	cv2.waitKey(3)



def main():
	rate = rospy.Rate(10) 
	

	while not rospy.is_shutdown():
		x = 0
		x += 1
		

if __name__ == '__main__':

	try:
		rospy.init_node('get_image')
		rospy.Subscriber('/zed/left/image_raw_color', Image, imageCallBack)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass
