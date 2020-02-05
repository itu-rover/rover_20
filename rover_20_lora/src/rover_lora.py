#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Getting:
#1 : wifi comm has break down


import rospy
import serial
import time
from std_msgs.msg import String
from geometry_msgs.msg import Twist

namespace = '[RoverLora_GroundStation : ] '
joyString = ""

def joyCallback(data):
	global joyString
	joyString = data.data




def lora():
	global joyString
	global namespace
	

	while not rospy.is_shutdown():


		ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE,
								 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)  # open serial
		ser.timeout = 0.4

		while ser.isOpen() and not rospy.is_shutdown():
			receive = ser.readline()
			print(namespace + receive)
			if receive == '1':
				print(" Select mode \n 1 : Autonomous \n 2 : CMD")
				mode = raw_input()

				if mode == '1':             #Send the wp
					receive = ser.readline()			
					print(namespace + "Reading : " + str(receive))
					rospy.sleep(1)




				elif mode == '2':         #Send joystring          
					
					while not rospy.is_shutdown():
						print(namespace + joyString)
						ser.writelines(joyString + "\n")
						ser.flushInput()
						ser.flushOutput()
						rospy.sleep(0.4)
			else:
				ser.writelines("waiting")
				rospy.sleep(1)








if __name__ == '__main__':
	try:
		rospy.init_node('rover_lora')
		rospy.Subscriber('/rover_serial_topic', String, joyCallback)
		lora()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")

