#!/usr/bin/env python
# -*- coding: utf-8 -*-


import rospy

from sensor_msgs.msg import Joy

class switcher(object) :
	def __init__(self) :

		rospy.init_node('keyboard_to_joystick')
		self.pub = rospy.Publisher("/joy", Joy, queue_size = 50)

		self.joy_msg = Joy()
		self.main()

		

	def case_1(self) :                         #up

		self.joy_msg.axes[7] =  1 
		
	def	case_2(self) :                         #down

		self.joy_msg.axes[7] = -1 
		
	def case_3(self) :                         #left 

		self.joy_msg.axes[6] =  1 
		
	def	case_4(self) :                         #right

		self.joy_msg.axes[6] = -1 
		
	def case_5(self) :                         #forward

		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    =  1 
		
	def case_6(self) :                         #backward

		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    = -1 
		
	def	case_7(self) :                         #up fast

		self.joy_msg.axes[7]    =  1
		self.joy_msg.buttons[2] =  1 
		
	def case_8(self) :                         #down fast
		
		self.joy_msg.axes[7]    = -1
		self.joy_msg.buttons[2] =  1 
		
	def case_9(self) :                         #left fast

		self.joy_msg.axes[6]    =  1
		self.joy_msg.buttons[2] =  1 
		
	def	case_10(self) :                        #right fast

		self.joy_msg.axes[6]    = -1
		self.joy_msg.buttons[2] =  1 
		
	def case_11(self) :                        #forward fast

		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    =  1 
		self.joy_msg.buttons[2] =  1 
		
	def case_12(self) :                        #backward fast
		
		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    = -1
		self.joy_msg.buttons[2] =  1 
		
	def	case_13(self) :                        #roll increase
		
		self.joy_msg.buttons[5] =  1
		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    =  1 
		
	def case_14(self) :                        #roll decrease
		
		self.joy_msg.buttons[5] =  1
		self.joy_msg.buttons[4] =  1
		self.joy_msg.axes[7]    = -1 
		
	def case_15(self) :                        #pitch increase
		
		self.joy_msg.buttons[5] =  1
		self.joy_msg.axes[6]    =  1 
		
	def	case_16(self) :                        #pitch decrease

		self.joy_msg.buttons[5] =  1
		self.joy_msg.axes[6]    = -1 
		
	def	case_17(self) :                        #yaw increase

		self.joy_msg.buttons[5] =  1 
		self.joy_msg.axes[7]    =  1 
		
	def	case_18(self) :                        #yaw decrease

		self.joy_msg.buttons[5] =  1 
		self.joy_msg.axes[7]    = -1 
		
	def case_19(self) :                        #open gripper

		self.joy_msg.buttons[3] =  1
		self.joy_msg.buttons[5] =  1 
		
	def	case_20(self) :                        #close gripper
		
		self.joy_msg.buttons[0] =  1
		self.joy_msg.buttons[5] =  1

	
	def main(self) :

		command = "1"

		while not rospy.is_shutdown() :

			self.joy_msg.axes    = [0, 0, 1, 0, 0, 1, 0, 0]                   #Logitech joystick message when any key is not pressed.
			self.joy_msg.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			print(" 1: up              11: forward fast")
			print(" 2: down            12: backward fast")
			print(" 3: left            13: roll increase")
			print(" 4: right           14: roll decrease")
			print(" 5: forward         15: pitch increase")       
			print(" 6: backward        16: pitch decrease")
			print(" 7: up fast         17: yaw increase")
			print(" 8: down fast       18: yaw decrease")
			print(" 9: left fast       19: open gripper")
			print("10: right fast      20: close gripper\n")
			
			print("Enter command")

			command = raw_input()

			if command == "-1" :

				break

			print("adim1")

			case_name = "case_" + command

			case = getattr(self, case_name, lambda: "invalid command")

			print("adim2")			
			
			
			case()

			print("adim3")			

			self.pub.publish(self.joy_msg)


if __name__ == '__main__':
	switcher()






