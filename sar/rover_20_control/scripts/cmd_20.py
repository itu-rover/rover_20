#!/usr/bin/env python
import rospy
import math
from std_msgs.msg import String
from geometry_msgs.msg import Twist

twist_cmd = Twist();
twist_nav = Twist();
twist = Twist();

pub=rospy.Publisher("/rover_serial_topic", String, queue_size=10)

def callback_cmd(data):
	#joystick
	twist_cmd.linear.x = data.linear.x * 90 #80  
	twist_cmd.angular.z = data.angular.z * 90 #80

def callback_nav(data):
	#autonomous
	twist_nav.linear.x = data.linear.x * 90 #80
	twist_nav.angular.z = data.angular.z * 90 #80

def main():
	rospy.init_node('rover_20_cmd_sub_serial')
	rospy.Subscriber("/cmd_vel", Twist, callback_nav)
	rospy.Subscriber("/joy_teleop/cmd_vel", Twist, callback_cmd)

	way_left="0"
	left_wheelString="000"
	way_right="000"
	right_wheelString="000"
	way_left = 0
	way_right = 0
	all_wheels_msg = ""
	robotic_arm_msg = "1000656515656552011665320002"
	science_msg = "3212321526541653"

	left_wheel = 0 # important
	right_wheel = 0 # important

	rate = rospy.Rate(10)

	while not rospy.is_shutdown():

		if(twist_cmd.linear.x != 0.0 or twist_cmd.angular.z != 0.0):
			twist = twist_cmd

		else:
			twist = twist_nav

		if twist.linear.x >= 0:

			left_wheel = twist.linear.x -  twist.angular.z
			right_wheel = twist.linear.x + twist.angular.z

			if(twist.angular.z != 0):
				if(abs(left_wheel) < 40):
					left_wheel = 40
				if(abs(right_wheel) < 40):
					right_wheel = 40

		elif twist.linear.x < 0: 

			left_wheel = twist.linear.x + twist.angular.z
			right_wheel = twist.linear.x - twist.angular.z

			if(twist.angular.z != 0):
				if(abs(left_wheel) < 40):
					left_wheel = 40
				if(abs(right_wheel) < 40):
					right_wheel = 40

		if(left_wheel < 0):
			way_left = 1
			left_wheel *= -1
		else:
			way_left = 0

		if(right_wheel < 0):
			way_right = 1
			right_wheel *= -1
		else:
			way_right = 0

		print("left: "+str(left_wheel)+ " right: "+ str(right_wheel) + " fark: "+str(abs(left_wheel - right_wheel)))
		
		if abs(left_wheel) < 10:
			left_wheelString = "00" + str(int(left_wheel))
			
		elif abs(left_wheel) < 100:
			left_wheelString = "0" + str(int(left_wheel))

		elif abs(left_wheel) > 100:
			left_wheelString = str(int(left_wheel))			

		if abs(right_wheel) < 10:
			right_wheelString = "00" + str(int(right_wheel))
			
		elif abs(right_wheel) < 100:
			right_wheelString = "0" + str(int(right_wheel))

		elif abs(right_wheel) > 100:
			right_wheelString = str(int(right_wheel))

		if(left_wheel > 200): #160
			left_wheelString = "200"

		if(right_wheel > 200): #160
			right_wheelString = "200"
		
		all_wheels_msg = str(way_left) + str(left_wheelString) + str(way_right) + str(right_wheelString)
		print("S"+ all_wheels_msg+ robotic_arm_msg + science_msg +"F")
		pub.publish("S"+ all_wheels_msg + robotic_arm_msg + science_msg +"F")
		rate.sleep()

if __name__ == '__main__':
	main()
