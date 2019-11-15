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

	while not rospy.is_shutdown():
		print("1: Take Picture \n ")
		userInput = raw_input()
		if userInput == "":
			controlPub.publish("1")


if __name__ == '__main__':

	try:
		rospy.init_node('rover_modelling_controller')
		controlPub = rospy.Publisher('/rover_modelling/control',String,queue_size=100)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass