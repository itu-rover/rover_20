#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Reads arm encoder data and publishes joint states.
#Encoder data must be in form of S + joint1 + joint2 + joint3 + joint4 + joint5 + joint6 + C + F
#Here, each joint has four digits and is in terms of degree.




import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from std_msgs.msg import Int8

import math


class joint_states(object):
	def __init__(self):



		rospy.init_node("real_joint_state_publisher")
		rospy.Subscriber("/arm_encoder", String, self.encoder_callback)
		self.pub = rospy.Publisher("/joint_states", JointState, queue_size = 50)

		self.joint_states = JointState()

		self.joint_states.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
		#self.joint_states.position = [1, 1, 1, 1, 1, 1]
		#self.joint_states.effort = [10, 10, 10, 10, 10, 10]

		self.joint1_offset = 0     #Difference between joint zero positions used by electronics and Moveit, in radian. 
		self.joint2_offset = 0
		self.joint3_offset = 0
		self.joint4_offset = 0
		self.joint5_offset = 0
		self.joint6_offset = 0

		self.rate = rospy.Rate(30)


		while not rospy.is_shutdown():
			
		
			self.state_publisher()
			print(self.joint_states)

			self.rate.sleep()

			

	def encoder_callback(self, data) :

		encoder = data.data

		
		joint1 = float(get_sign(encoder[1])*int(encoder[2:5])*math.pi/180)    + float(self.joint1_offset)    #joint states in radian
		joint2 = float(get_sign(encoder[5])*int(encoder[6:9])*math.pi/180)    + float(self.joint2_offset)
		joint3 = float(get_sign(encoder[9])*int(encoder[10:13])*math.pi/180)  + float(self.joint3_offset)
		joint4 = float(get_sign(encoder[13])*int(encoder[14:17])*math.pi/180) + float(self.joint4_offset)
		joint5 = float(get_sign(encoder[17])*int(encoder[18:21])*math.pi/180) + float(self.joint5_offset)
		joint6 = float(get_sign(encoder[21])*int(encoder[22:25])*math.pi/180) + float(self.joint6_offset)

		joint1 = change_range(joint1)   #Changes joint state range to [-pi, pi]
		joint2 = change_range(joint2)
		joint3 = change_range(joint3)
		joint4 = change_range(joint4)
		joint5 = change_range(joint5)
		joint6 = change_range(joint6)
		
				
		self.joint_states.position = [joint1, joint2, joint3, joint4, joint5, joint6]


	def state_publisher(self) :

		self.pub.publish(self.joint_states)


"""def elk_to_rad(joint_elk, elk_min, elk_max, deg_min, deg_max) :

	joint_deg = (joint_elk - elk_min)*(deg_max - deg_min)/(elk_max - elk_min) + deg_min

	return joint_deg*math.pi/180"""

def get_sign(number) :  
		
	if number == '0' :

		return int(-1)

	elif number == '1' :

		return int(1)

def change_range(joint) :

	while abs(joint) > math.pi :

		joint += 2*math.pi

	return joint	



if __name__ == '__main__':
	joint_states()
