#!/usr/bin/env python
#This is the Modelling Code  for ITU Rover Team
##This code takes pictures with pressing space bar and mark the gps data to their exif's.
###This code is the primary code for modelling and scaling for science task that will be done on another operating system.



import numpy as np
import imutils
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist

def main():

	twist = Twist()
	twist.linear.x = 0
	twist.angular.z = 0
	count = 0
	rospy.init_node('cmd_vel_zero')
	rate = rospy.Rate(10)
	pub = rospy.Publisher('/cmd_vel',Twist,queue_size=10)
	while not rospy.is_shutdown():
		pub.publish(twist)
		count +=1
		if count >5:
			break
		rate.sleep()


if __name__ == '__main__':
	
	main()