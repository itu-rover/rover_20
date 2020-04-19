#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Used for controlling 6-axis robotic arm (position control) with forward kinematics by using Logitech joystick. Reads encoder data, changes it (increases or decreases joint states) according to joystick command and adds gripper command.
#Publishes to /arm_19_ui and /arm_19_serial in form of S + joint1 + joint2 + joint3 + joint4 + joint5 + joint6 + gripper_command + C + F
#Here, each joint has three digits and is in terms of unit used by electronics.
#gripper_command is 0 for closing gripper, 1 for opening gripper and 2 for stopping gripper.
#If any command is not given from joystick, encoder data is published back to the serial and gripper_command remains as 2.

import rospy
from std_msgs.msg import String

from sensor_msgs.msg import Joy
from sensor_msgs.msg import JointState

import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3




class arm_serial(object):
	def __init__(self):

		self.joint1 = 40
		self.joint2 = 40                  #initial degree value of joint2
		self.joint3 = 0                  #initial degree value of joint3
		self.joint4 = 40
		self.joint5 = 40
		self.joint6 = 40

		self.gripper_command = "2"        #Indicates gripper is at the steady state.


		self.joint1_serial = "0000"
		self.joint2_serial = "0000"        #initial serial for joint2
		self.joint3_serial = "1060"        #initial serial for joint3
		self.joint4_serial = "0000"
		self.joint5_serial = "0000"
		self.joint6_serial = "0000"

		self.velocity_scale_1 = 3
		self.velocity_scale_2 = 3
		self.velocity_scale_3 = 3
		self.velocity_scale_4 = 3
		self.velocity_scale_5 = 3
		self.velocity_scale_6 = 3

		self.joint1_offset = 0            #Difference between zero positions of joints between electronics and software, in degree
		self.joint2_offset = 0
		self.joint3_offset = 0
		self.joint4_offset = 0
		self.joint5_offset = 0
		self.joint6_offset = 0


		self.new_message_1 = False
		self.new_message_2 = False
		self.new_message_3 = False
		self.new_message_4 = False
		self.new_message_5 = False
		self.new_message_6 = False


		self.elk_control_1 = 0
		self.elk_control_2 = 0
		self.elk_control_3 = 0
		self.elk_control_4 = 0
		self.elk_control_5 = 0
		self.elk_control_6 = 0

		rospy.init_node('rover_arm_fk')

		rospy.Subscriber("/arm_encoder", String, self.arm_callback)
		#rospy.Subscriber("/joint_states", JointState, self.arm_callback)   Should we subscribe /joint_states or use encoder data directly???
		#rospy.Subscriber("/encoder2", String, self.callbackarm2)
		#rospy.Subscriber("/encoder3", String, self.callbackarm3)
		#rospy.Subscriber("/encoder4", String, self.callbackarm4)
		#rospy.Subscriber("/encoder5", String, self.callbackarm5)
		#rospy.Subscriber("/encoder6", String, self.callbackarm6)

		rospy.Subscriber("/joy", Joy, self.joy_callback)

		self.pub = rospy.Publisher("/arm_19_serial", String, queue_size = 50)
		#self.pub2 = rospy.Publisher("/rover_serial_arm2", String, queue_size=50)
		#self.pub3 = rospy.Publisher("/rover_serial_arm3", String, queue_size=50)
		#self.pub4 = rospy.Publisher("/rover_serial_arm4", String, queue_size=50)
		#self.pub5 = rospy.Publisher("/rover_serial_arm5", String, queue_size=50)
		#self.pub6 = rospy.Publisher("/rover_serial_arm6", String, queue_size=50)



		self.pub_ui = rospy.Publisher("/arm_19_ui", String, queue_size = 50)


		self.main()

		#rospy.spin()


	def arm_callback(self, data):

		encoder = data.data

		self.joint3 = get_sign(encoder[1])*int(encoder[2:5])    + self.joint1_offset    #joint states in degree
		#self.joint2 = get_sign(encoder[5])*int(encoder[6:9])    + self.joint2_offset
		##self.joint3 = get_sign(encoder[9])*int(encoder[10:13])  + self.joint3_offset
		#self.joint4 = get_sign(encoder[13])*int(encoder[14:17]) + self.joint4_offset
		#self.joint5 = get_sign(encoder[17])*int(encoder[18:21]) + self.joint5_offset
		#self.joint6 = get_sign(encoder[21])*int(encoder[22:25]) + self.joint6_offset

		"""joint1_elk = encoder[1:4]
		joint2_elk = encoder[4:7]
		joint3_elk = encoder[7:10]
		joint4_elk = encoder[10:13]
		joint5_elk = encoder[13:16]
		joint6_elk = encoder[16:19]

		self.joint1 = elk_to_deg(int(joint1_elk),  ,  ,  ,  ) #joint states in degree
		self.joint2 = elk_to_deg(int(joint2_elk),  ,  ,  ,  )
		self.joint3 = elk_to_deg(int(joint3_elk),  ,  ,  ,  )
		self.joint4 = elk_to_deg(int(joint4_elk),  ,  ,  ,  )
		self.joint5 = elk_to_deg(int(joint5_elk),  ,  ,  ,  )
		self.joint6 = elk_to_deg(int(joint6_elk),  ,  ,  ,  )"""


	"""def callbackarm2(self, data):

		encoder = data.data

		elk = encoder[1:4]
		print("joint2_elk:" + elk)
		self.joint2 = invfunc(int(elk)) #degree value of joint 2
			#pub = rospy.Publisher("/rover_joint_state_publisher_2", String, queue_size=50)
			#pub.publish(joint2)


	def callbackarm3(self,data):

		encoder = data.data

		elk = encoder[1:4]
		print("joint3_elk:" + elk)
		self.joint3 = invfunc(int(elk)) #degree value of joint 3
		#pub = rospy.Publisher("/rover_joint_state_publisher_3", String, queue_size=50)
			#pub.publish(joint3)

	def callbackarm4(self, data):

		encoder = data.data

		elk = encoder[1:4]
		print("joint4_elk:" + elk)
		self.joint4 = invfunc(int(elk)) #degree value of joint 4

	def callbackarm5(self, data):

		encoder = data.data

		elk = encoder[1:4]
		print("joint5_elk:" + elk)
		self.joint5 = invfunc(int(elk)) #degree value of joint 5

	def callbackarm6(self, data):

		encoder = data.data

		elk = encoder[1:4]
		print("joint6_elk:" + elk)
		self.joint6 = invfunc(int(elk)) #degree value of joint 6"""


	#def elk_to_deg(x):
	#	return (x/11.23)+34



	def joy_callback(self, data):

		self.gripper_command = "2"


		if data.buttons[5]== 1 and data.buttons[3]== 1 :                                       #Open gripper

			self.gripper_command = "1"

		elif data.buttons[5]== 1 and data.buttons[0]== 1 :                                     #Close gripper

			self.gripper_command = "0"


		elif data.buttons[2]==1 and data.buttons[5]==0 and data.axes[0]!=0 :                                           #Increase/decrease joint1.

			self.joint1 = self.joint1 + int(data.axes[0]*self.velocity_scale_1)

			if self.joint1 > 108 :
				self.joint1 = 108

			if self.joint1 < 40 :
				self.joint1 = 40

			"""self.elk_control_1 = 831*(self.joint1-34)/74


			if (self.elk_control_1 > 831) :
				self.elk_control_1 = 831

			if (self.elk_control_1 < 60) :
				self.elk_control_1 = 60"""


			self.joint1_serial = floattostring(self.joint1)


			self.new_message_1 = True



		elif data.buttons[3]==1 and data.axes[1]!=0 :                                        #Increase/decrease joint2.

			self.joint2 = self.joint2 + int(data.axes[1]*self.velocity_scale_2)

			if self.joint2 > 108 :
				self.joint2 = 108

			if self.joint2 < 40 :
				self.joint2 = 40


			"""self.elk_control_2 = 831*(self.joint2-34)/74


			if (self.elk_control_2 > 831) :
				self.elk_control_2 = 831

			if (self.elk_control_2 < 60) :
				self.elk_control_2 = 60"""


			self.joint2_serial = floattostring(self.joint2)


			self.new_message_2 = True


		elif data.buttons[1]==1 and data.axes[1]!=0 and data.buttons[5]==0 :                                           #Increase/decrease joint3.

			self.joint3 = self.joint3 + int(data.axes[1]*self.velocity_scale_3)

			if self.joint3 > 60 :
				self.joint3 = 108

			if self.joint3 < -60 :
				self.joint3 = 40



			"""self.elk_control_3 = 831*(self.joint3-34)/74


			if (self.elk_control_3 > 831) :
				self.elk_control_3 = 831

			if (self.elk_control_3 < 60) :
				self.elk_control_3 = 60"""


			self.joint3_serial = floattostring( self.joint3 )


			self.new_message_3 = True


		elif data.buttons[0]==1 and data.axes[0]!=0 :

			self.joint4 = self.joint4 + int(data.axes[0]*self.velocity_scale_4)

			if self.joint4 > 108 :
				self.joint4 = 108

			if self.joint4 < 40 :
				self.joint4 = 40

			"""self.elk_control_4 = 831*(self.joint4-34)/74


			if (self.elk_control_4 > 831) :
				self.elk_control_4 = 831

			if (self.elk_control_4 < 60) :
				self.elk_control_4 = 60"""


			self.joint4_serial = floattostring(self.joint4)


			self.new_message_4 = True


		elif data.buttons[2]==1 and data.buttons[5]==1 and data.axes[1]!=0 :

			self.joint5 = self.joint5 + int(data.axes[1]*self.velocity_scale_5)

			if self.joint5 > 108 :
				self.joint5 = 108

			if self.joint5 < 40 :
				self.joint5 = 40

			"""self.elk_control_5 = 831*(self.joint5-34)/74


			if (self.elk_control_5 > 831) :
				self.elk_control_5 = 831

			if (self.elk_control_5 < 60) :
				self.elk_control_5 = 60"""


			self.joint5_serial = floattostring(self.joint5)


			self.new_message_5 = True


		elif data.buttons[1]==1 and data.buttons[5]==1 and data.axes[0]!=0 :

			self.joint6 = self.joint6 + int(data.axes[0]*self.velocity_scale_6)

			if self.joint6 > 108 :
				self.joint6 = 108

			if self.joint6 < 40 :
				self.joint6 = 40

			"""self.elk_control_6 = 831*(self.joint6-34)/74


			if (self.elk_control_6 > 831) :
				self.elk_control_6 = 831

			if (self.elk_control_6 < 60) :
				self.elk_control_6 = 60"""


			self.joint6_serial = floattostring(self.joint6)


			self.new_message_6 = True



		print("joint1_deg        :" + str(self.joint1) + "     " + "joint2_deg        :" + str(self.joint2))
		print("joint3_deg        :" + str(self.joint3) + "     " + "joint4_deg        :" + str(self.joint4))
		print("joint5_deg        :" + str(self.joint5) + "     " + "joint6_deg        :" + str(self.joint6)+"\n")

		#print("joint1_elk_control:" + str(self.elk_control_1) + "     " + "joint2_elk_control:" + str(self.elk_control_2))
		#print("joint3_elk_control:" + str(self.elk_control_3) + "     " + "joint4_elk_control:" + str(self.elk_control_4))
		#print("joint5_elk_control:" + str(self.elk_control_5) + "     " + "joint6_elk_control:" + str(self.elk_control_6)+"\n")

		print("gripper_command   :" + self.gripper_command + "\n")








	def main(self):

		rate = rospy.Rate(5) #10 Hz

		while not rospy.is_shutdown():

			"""if (self.joint2_serial > 831):
				self.joint2_serial = 831
			if (self.joint2_serial < 0):
				self.joint2_serial = 000

			if (self.joint3_serial > 831):
				self.joint3_serial = 831
			if (self.joint3_serial < 0):
				self.joint3_serial = 000"""

			self.pub.publish(self.joint1_serial+self.joint2_serial+self.joint3_serial+self.joint4_serial+self.joint5_serial+self.joint6_serial)
			self.pub_ui.publish(self.joint1_serial+" "+self.joint2_serial+" "+self.joint3_serial+" "+self.joint4_serial+" "+self.joint5_serial+" "+self.joint6_serial+" "+self.gripper_command)

			self.gripper_command = "2"

			"""if self.new_message_1 :

				self.pub1.publish("S"+str(self.joint1_serial)+"C"+"F")

				self.new_message_1 = False



			if self.new_message_2 :

				self.pub2.publish("S"+str(self.joint2_serial)+"C"+"F")

				self.new_message_2 = False



			if self.new_message_3 :

				self.pub3.publish("S"+str(self.joint3_serial)+"C"+"F")

				self.new_message_3 = False


			if self.new_message_4 :

				self.pub4.publish("S"+str(self.joint4_serial)+"C"+"F")

				self.new_message_4 = False


			if self.new_message_5 :

				self.pub5.publish("S"+str(self.joint5_serial)+"C"+"F")

				self.new_message_5 = False


			if self.new_message_6 :

				self.pub6.publish("S"+str(self.joint6_serial)+"C"+"F")

				self.new_message_6 = False"""



			rate.sleep()


"""def elk_to_deg(joint_elk, elk_min, elk_max, deg_min, deg_max) :

	joint_deg = (joint_elk - elk_min)*(deg_max - deg_min)/(elk_max - elk_min) + deg_min

	return joint_deg

def deg_to_elk(joint_deg, deg_min, deg_max, elk_min, elk_max) :

	joint_elk = (joint_deg - deg_min)*(elk_max - elk_min)/(deg_max - deg_min) + elk_min

	return joint_elk"""


def floattostring(joint):

	value = int(joint)

	if value < 0 :

		value = (-1)*value

		if value < 10 :

			string = "000" + str(value)

		elif value < 100 :

			string = "00" + str(value)

		elif value < 1000 :

			string = "0" + str(value)

	else :

		if value < 10 :

			string = "100" + str(value)

		elif value < 100 and value > 9 :

			string = "10" + str(value)

		elif value < 1000 :

			string = "1" + str(value)

	return string

def get_sign(number):

	if number == '0' :

		return int(1)

	elif number == '1' :

		return int(-1)

if __name__ == '__main__':
	arm_serial()
