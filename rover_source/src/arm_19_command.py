#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Subscribes /rover_arm_controller/state and /gripper_command19 topics, publishes joint states and gripper command to serial and ui.

#         Positive Directions of Joints According to Moveit              Zero Positions
#joint1:  CW positive (looked from top)                                     3.14          Opposite
#joint2:  increases in positive direction (Arm moves upward)                0.78          Opposite
#joint3:  Arm collapses in positive direction                               0.73          Opposite
#joint4:  Gripper moves CW in positive direction (looked from top)          0.00          Opposite
#joint5:  Gripper moves upward in positive direction (looked from back)     0.00          Opposite
#joint6:  Gripper moves CW in positive direction (looked from back)         0.00          Same




import rospy
from control_msgs.msg import JointTrajectoryControllerState
from std_msgs.msg import String
from std_msgs.msg import Int8

import math


class joint_commands(object):
	def __init__(self):



		rospy.init_node("arm_19_command_publisher")
		rospy.Subscriber("/rover_arm_controller/state", JointTrajectoryControllerState, self.arm_callback)
		rospy.Subscriber("/gripper_command19", Int8, self.gripper_callback)
		
		self.pub = rospy.Publisher("/arm_19_serial", String, queue_size = 50)
		self.pub_ui = rospy.Publisher("/arm_19_ui", String, queue_size = 50)

		self.joint1_str = "0000"
		self.joint2_str = "0000"           
		self.joint3_str = "0000"         #These values must be set to minimum joint_str
		self.joint4_str = "0000"
		self.joint5_str = "0000"
		self.joint6_str = "0000"

		self.gripper_command = "2"

		self.rate = rospy.Rate(30)


		while not rospy.is_shutdown():
			
		
			self.command_publisher()
			#print(self.joint_commands)

			self.rate.sleep()

			

	def arm_callback(self, command) :

		#command = data.data

		joint1 = command.desired.positions[0]  #Change positions to velocities for velocity control
		joint2 = command.desired.positions[1]
		joint3 = command.desired.positions[2]
		joint4 = command.desired.positions[3]
		joint5 = command.desired.positions[4]
		joint6 = command.desired.positions[5]

					
		joint1_elk = (-1)*rad_to_elk(joint1, -180, 180,  0) #-179.905176858)     #This part needs to be updated according to the mapping used by electronics. 
		joint2_elk = (-1)*rad_to_elk(joint2, -180, 180,  0) #-45.0091523146)     #Offset values must be found by using Moveit Setup Assistant. 
		joint3_elk = (-1)*rad_to_elk(joint3, -180, 180,  0) #-41.5122054923)
		joint4_elk = (-1)*rad_to_elk(joint4, -180, 180,  0)
		joint5_elk = (-1)*rad_to_elk(joint5, -180, 180,  0)
		joint6_elk = rad_to_elk(joint6, -180, 180,  0)

		print("joint1: " + str(joint1_elk))
		print("joint2: " + str(joint2_elk))
		print("joint3: " + str(joint3_elk))
		print("joint4: " + str(joint4_elk))
		print("joint5: " + str(joint5_elk))
		print("joint6: " + str(joint6_elk) + "\n")

		self.joint1_str = floattostring(joint1_elk)
		self.joint2_str = floattostring(joint2_elk)
		self.joint3_str = floattostring(joint3_elk)
		self.joint4_str = floattostring(joint4_elk)
		self.joint5_str = floattostring(joint5_elk)
		self.joint6_str = floattostring(joint6_elk)


	def gripper_callback(self, data) :

		self.gripper_command = str(data.data)

		

	

	def command_publisher(self) :

		self.pub.publish(self.joint1_str+self.joint2_str+self.joint3_str+self.joint4_str+self.joint5_str+self.joint6_str+self.gripper_command)
		self.pub_ui.publish(self.joint1_str+" "+self.joint2_str+" "+self.joint3_str+" "+self.joint4_str+" "+self.joint5_str+" "+self.joint6_str+" "+self.gripper_command)


"""def rad_to_elk(joint_rad, rad_min, rad_max, elk_min, elk_max) :              #Converts joint states from rad to elk unit and constrains the result

	joint_elk = (joint_rad - rad_min)*(elk_max - elk_min)/(rad_max - rad_min) + elk_min

	if joint_elk < elk_min :

		joint_elk = elk_min

	if joint_elk > elk_max :

		joint_elk = elk_max

	return joint_elk"""

def rad_to_elk(joint_rad, elk_min, elk_max, joint_offset) :                      #Converts joint states from rad to elk unit and constrains the result

	joint_elk = joint_rad*(180/math.pi) + joint_offset

	while abs(joint_elk) > 180 :

		joint_elk += 360

	if joint_elk < elk_min :

		joint_elk = elk_min

	if joint_elk > elk_max :

		joint_elk = elk_max

	return joint_elk





def floattostring(joint):

	value = int(joint)
	
	if value > 0 :

		if value < 10 :

			string = "000" + str(value)

		elif value < 100 :

			string = "00" + str(value)

		elif value < 1000 :

			string = "0" + str(value)

	else :

		value = (-1)*value
		
		if value < 10 :
			
			string = "100" + str(value)
		
		elif value < 100 and value > 9 :
			
			string = "10" + str(value)
		
		elif value < 1000 :
			
			string = "1" + str(value)
		
	return string



if __name__ == '__main__':
	joint_commands()
