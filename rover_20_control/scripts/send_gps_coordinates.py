#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2018 ERC sends 2d coordinates into  ref frame
# ITU Rover Team
import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
import actionlib
import tf
from sensor_msgs.msg import NavSatFix


waypoint = NavSatFix()


def move():
	
	Pub = rospy.Publisher('/rover_gps/waypoint', NavSatFix, queue_size=10)

	while not rospy.is_shutdown():
		
		print("enter lat")
		string_x = raw_input()
		print("Enter long ")
		string_y = raw_input()

		waypoint.latitude = float(string_y) #29.0233425
		waypoint.longitude = float(string_x) #41.1051722

		Pub.publish(waypoint)	


if __name__ == '__main__':
	try:
		rospy.init_node('send_coordinates')
		move()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")

