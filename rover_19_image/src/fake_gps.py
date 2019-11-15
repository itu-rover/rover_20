#!/usr/bin/env python
#This is the Modelling Code  for ITU Rover Team
##This code takes pictures with pressing space bar and mark the gps data to their exif's.
###This code is the primary code for modelling and scaling for science task that will be done on another operating system.



import numpy as np
import imutils
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix

def main():

	navMsg = NavSatFix()
	navMsg.header.frame_id = "map"
	navMsg.header.stamp = rospy.Time.now()
	navMsg.latitude =40.514689
	navMsg.longitude = -111.502291
	while not rospy.is_shutdown():
		gpsPub.publish(navMsg)


if __name__ == '__main__':

	try:
		rospy.init_node('fake_gps')
		rate = rospy.Rate(10)
		gpsPub = rospy.Publisher('/gps/fix',NavSatFix,queue_size=50)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass