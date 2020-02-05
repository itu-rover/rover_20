#!/usr/bin/env python
# -*- coding: utf-8 -*-
#sending : 
#1 = wifi comm has breakdown

import rospy
import serial
import time
from std_msgs.msg import String
import rosparam
from sensor_msgs.msg import NavSatFix
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionResult
from actionlib_msgs.msg import GoalStatusArray

namespace = '[RoverLora_Rover : ] '
loraMsg = 0
currGps = NavSatFix()
currCmd = Twist()
currResult = MoveBaseActionResult()


#get data from pc
def loraCallback(data):
	global loraMsg
	loraMsg = int(data.data)

def gpsCallback(data):
	global currGps
	currGps = data

def cmdCallback(data):
	global currCmd
	currCmd = data

def resultCallback(data):
	global currResult
	currResult = data

def letsSerial():
	rospy.init_node("rover_lora2")

	global namespace
	global loraMsg
	global currResult, currCmd, currGps



	rospy.Subscriber("/lora/checkout", String, loraCallback)
	rospy.Subscriber("/gps/fix", NavSatFix, gpsCallback)
	rospy.Subscriber("/cmd_vel", Twist, cmdCallback)
	rospy.Subscriber("/move_base/result", MoveBaseActionResult, resultCallback)
	count = 0

	while not rospy.is_shutdown():


		ser = serial.Serial(port='/dev/ttyUSB1', baudrate=9600, parity=serial.PARITY_NONE,
								 stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)  # open serial
		ser.timeout = 0.4
		sendCount = 0
		while ser.isOpen() and not rospy.is_shutdown():
			
			dataOld = loraMsg
			rospy.sleep(2)
			dataNew = loraMsg
			differentiate = dataNew - dataOld
			print(namespace + "differentiate : " + str(differentiate) +" data : "+ str(dataNew))
			if differentiate == 0:
				count += 1

			while count > 2 and not rospy.is_shutdown():
				receive = ser.readline()
				print("Wi-fi has break down")
				ser.writelines("1" + "\n")
				ser.flushInput()
				ser.flushOutput()
				rospy.sleep(0.5)
				
				"""
				else:
					#receive = ser.readline()
					#print(namespace + receive)
					if receive == "autonomous" :                        
						while not rospy.is_shutdown():
							print("On autonomous state")
							ser.writelines("A/"+str(currGps.latitude)+"/"+str(currGps.longitude)+"/"+str(currCmd.linear.x)+"/"+str(currCmd.angular.z)+"\n")

							ser.flushInput()
							ser.flushOutput()
							rospy.sleep(0.5)"""
							




			#receive = ser.readline()
			#ser.writelines("1" + "\r\n")

			

			#ser.flushInput()
			#ser.flushOutput()

			




	rospy.spin()




if __name__ == '__main__':
	try:
		letsSerial()
	except rospy.ROSInterruptException:
		pass