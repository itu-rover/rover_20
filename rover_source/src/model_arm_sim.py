#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Used for controlling robotic arm in simulation via model arm. Subscribes Arduino rosserial topic "/chatter", takes joint state values of model arm and sends them to individual controllers as command



import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from std_msgs.msg import Int8
from std_msgs.msg import Float64
#from control_msgs.msg import JointTrajectoryControllerState

import math

def get_sign(number):  
		
	if number == '0' :

		return int(-1)

	elif number == '1' :

		return int(1)


class joint_states(object):
	def __init__(self):



		rospy.init_node("arm_19_command_publisher")
		rospy.Subscriber("/chatter", String, self.potentiometer_callback)  #subscribes Arduino rosserial topic

		self.joint1 = 0
		self.joint2 = 0
		self.joint3 = 0
		self.joint4 = 0
		self.joint5 = 0
		self.joint6 = 0
		
		self.pub1 = rospy.Publisher("/rover_arm_eksen1_joint_position_controller/command", Float64, queue_size = 50)
		self.pub2 = rospy.Publisher("/rover_arm_eksen2_joint_position_controller/command", Float64, queue_size = 50)
		self.pub3 = rospy.Publisher("/rover_arm_eksen3_joint_position_controller/command", Float64, queue_size = 50)
		self.pub4 = rospy.Publisher("/rover_arm_eksen4_joint_position_controller/command", Float64, queue_size = 50)
		self.pub5 = rospy.Publisher("/rover_arm_eksen5_joint_position_controller/command", Float64, queue_size = 50)
		self.pub6 = rospy.Publisher("/rover_arm_eksen6_joint_position_controller/command", Float64, queue_size = 50)

		#self.joint_states = JointTrajectoryControllerState()

		#self.joint_states.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
		
		#self.joint_states.position = [1, 1, 1, 1, 1, 1]
		#self.joint_states.effort = [10, 10, 10, 10, 10, 10]

		self.rate = rospy.Rate(30) #indicates running frequency of the code in Hertz


		while not rospy.is_shutdown():
			
		
			

			self.pub1.publish(self.joint1)
			self.pub2.publish(self.joint2)
			self.pub3.publish(self.joint3)
			self.pub4.publish(self.joint4)
			self.pub5.publish(self.joint5)
			self.pub6.publish(self.joint6)
			
			

			#self.rate.sleep()

			

	def potentiometer_callback(self, data) :

		potentiometer = data.data

		# The string "potentiometer" is in the form of S + joint1_deg + joint2_deg + joint3_deg + joint4_deg + joint5_deg + joint6_deg + CF
		# Each joint_deg starts with 0 or 1. 0 indicates negative, 1 indicates positive.

		self.joint1 = float(get_sign(potentiometer[1])*int(potentiometer[2:5])*math.pi/180)    #joint states in radian
		self.joint2 = float(get_sign(potentiometer[5])*int(potentiometer[6:9])*math.pi/180)
		self.joint3 = float(get_sign(potentiometer[9])*int(potentiometer[10:13])*math.pi/180)
		self.joint4 = float(get_sign(potentiometer[13])*int(potentiometer[14:17])*math.pi/180)
		self.joint5 = float(get_sign(potentiometer[17])*int(potentiometer[18:21])*math.pi/180)
		self.joint6 = float(get_sign(potentiometer[21])*int(potentiometer[22:25])*math.pi/180)

		
		#self.joint1 = float(potentiometer[1:5])*math.pi/180
		#self.joint2 = float(potentiometer[5:9])*math.pi/180
		#self.joint3 = float(potentiometer[9:13])*math.pi/180
		#self.joint4 = float(potentiometer[13:17])*math.pi/180
		#self.joint5 = float(potentiometer[17:21])*math.pi/180
		#self.joint6 = float(potentiometer[21:25])*math.pi/180

		#self.joint1 = float(potentiometer[1:4])*math.pi/180
		#self.joint2 = float(potentiometer[4:7])*math.pi/180
		#self.joint3 = float(potentiometer[7:10])*math.pi/180
		#self.joint4 = float(potentiometer[10:13])*math.pi/180
		#self.joint5 = float(potentiometer[13:16])*math.pi/180
		#self.joint6 = float(potentiometer[16:19])*math.pi/180

		

		# """

		# joint1_int = int(joint1_elk)
		# joint2_int = int(joint2_elk)
		# joint3_int = int(joint3_elk)
		# joint4_int = int(joint4_elk)
		# joint5_int = int(joint5_elk)
		# joint6_int = int(joint6_elk)

		

		# joint1 = ((joint1_int - 0 )(90-(-90))/(1008)+90)*math.pi/180
		# joint2 = (joint2_int - 460)(84-15)/(-1008) + 90

		# joint1 = joint1_int - 50
		# joint2 = joint2_int - 50
		# joint3 = joint3_int - 50
		# joint4 = joint4_int - 50
		# joint5 = joint5_int - 50
		# joint6 = joint6_int - 50


		# joint1 = elk_to_rad(joint1_int, 0, 1008, 90, -90)
		# joint2 = elk_to_rad(joint2_int, 460, 675, 84, 15)
		# joint3 = elk_to_rad(joint3_int,710, 920, 104, 55 )
		# joint4 = elk_to_rad(joint4_int, 1008, 20, -90, 180)
		# joint5 = elk_to_rad(joint5_int, 870, 550, 90, 0)
		# joint6 = elk_to_rad(joint6_int, 0, 1008, 90, -90)
		
		# joint1 = elk_to_rad(joint1_elk, 0, 1008, 90, -90)
		# joint2 = elk_to_rad(joint2_elk, 460, 675, 84, 15)
		# joint3 = elk_to_rad(joint3_elk,710, 920, 104, 55 )
		# joint4 = elk_to_rad(joint4_elk, 1008, 20, -90, 180)
		# joint5 = elk_to_rad(joint5_elk, 870, 550, 90, 0)
		# joint6 = elk_to_rad(joint6_elk, 0, 1008, 90, -90)
		




		# self.joint_states.desired.positions = [joint1, joint2, joint3, joint4, joint5, joint6]
		# """


	


# def elk_to_rad(joint_elk, elk_min, elk_max, deg_min, deg_max) :

# 		joint_deg = (joint_elk - elk_min)(deg_max - deg_min)/(elk_max - elk_min) + deg_min

# 		return joint_deg*math.pi/180

# def elk_to_rad1(joint_elk, elk_min, elk_max, deg_min, deg_max) :

# 		joint_deg = (joint_elk - elk_min)(deg_max - deg_min)/(elk_max - elk_min) + deg_min

# 		return joint_deg*math.pi/180

	
	


if __name__ == '__main__':
	joint_states()
