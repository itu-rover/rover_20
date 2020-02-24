#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionResult
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped, Twist
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import tf
from rover20_state_mach.msg import StateMsg
import time


class Approacher():
	def __init__(self):
		rospy.init_node('approach', anonymous=False)
		self.currPosX=0
		self.currPosY=0
		self.currPosZ=0
		self.yaw=0
		self.bearingToartag=0.0
		self.bearingToartag_old=0.0
		self.counter=0
		self.send_once=1
		self.artag_is_found=0
		self.sc = 3
		self.sum = 0
		self.average = 0
		self.bearing_counter = 0 #new
		self.approaching = False

		self.msg="-"
		self.state=StateMsg()
		self.move_msg= MoveBaseActionResult()
		self.twist = Twist()
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		print("waiting client server")
		self.client.wait_for_server()
		print(" client is on")
		rate = rospy.Rate(10) # 10hz
		#tell the action client that we want to spin a thread by default
		self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #Publish Nav Goal to ROS topic
		self.Pub2=rospy.Publisher('/artag_reach_topic',String,queue_size=10)  #Publisher oluşturduk
		self.done_topic = rospy.get_param('RoverSmach20/sub_topics/sub_done_approach', '/done_topic')
		#self.count = 0
		self.done_pub = rospy.Publisher(self.done_topic, String, queue_size = 10)
		self.middle_point = []
		self.artag_search_finish = False


		while not rospy.is_shutdown():

			rospy.Subscriber('/outdoor_waypoint_nav/odometry/filtered',Odometry, self.robotPoseSubscriber)
			rospy.Subscriber('/rover_state_topic',StateMsg, self.stateSubscriber)
			rospy.Subscriber('/stage_counter_topic', String, self.stagec_callback)
			rospy.Subscriber('/bearing_to_artag',String, self.artagYawSubscriber)
			rospy.Subscriber('/artag_search_done',String, self.artagSearchSubscriber)
			#rospy.Subscriber('/move_base/result',MoveBaseActionResult, self.moveSubscriber)

			print(self.artag_search_finish)
			
			#self.msg=self.artagYawSubscriber
			'''self.state.state=self.state.REACH_IMAGE '''   #changed
			if self.artag_search_finish == True:#if(self.state.state==self.state.REACH_ARTAG or self.state.state==self.state.APPROACH):
				#print(self.state.state)     #eklendi
				#print(self.state)
				if(self.msg=="-"):
					if self.approaching == False:
						print("artag is not found")
						twist_empty=Twist()
						self.Pub.publish(twist_empty)
						self.Pub2.publish("0")    #eklendi
					else:
						self.approaching = False
						self.go_forward_for3()

				else:
					'''for i in range(10):
						rospy.Subscriber('/bearing_to_artag',String, self.artagYawSubscriber)
						self.middle_point.append(int(self.msg))
						self.sum = self.sum + middle_point[i]
						self.average = self.sum/10
						print(middle_point[i])'''

					print(self.msg)   #self.msg
					#bear = abs(float(self.msg))
					bear = abs(float(self.msg))#abs(self.average)
					self.bearingToartag= float(self.msg)*pi /180 # AVERAGE REMOVED
					self.Pub2.publish("0")     #eklendi

					if bear> 5 and self.bearing_counter == 0:
						self.approaching = False

						self.rotate_to_ball_2()

					elif bear <= 5:
						self.approaching = True

						self.twist.angular.z=0
						self.Pub.publish(self.twist)
						self.Pub2.publish("0")      #eklendi
						#if(self.count<3):#3
						if(self.sc ==3):
							self.go_forward()
							self.done_pub.publish("1")

						if(self.sc >= 4):
							self.go_forward()
							self.done_pub.publish("1")

						while not rospy.is_shutdown():
							print("Succesful")
							#self.Pub2.publish("1")
							break
							 #degistirildi
						self.bearing_counter += 1
			#rospy.spin()   

	def stateSubscriber(self,stateMsg):
		self.state=stateMsg

	def stagec_callback(self, data):
		self.sc = float(data.data)

	def moveSubscriber(self,moveMsg):
		self.move_msg=moveMsg.data
		# print(self.move_msg.status.text)

	def artagYawSubscriber(self,yawMsg):
		# LET MURRUVET KNOW THIA ERROR
		self.msg= yawMsg.data

	def artagSearchSubscriber(self, data):
		self.artag_search_done = data.data
		if self.artag_search_done == "1":
			self.artag_search_finish = True
		else:
			self.artag_search_finish = False

	def robotPoseSubscriber(self,poseMsg): #Odometry update recieved from ROS topic, run this function
	
		self.currPosX = poseMsg.pose.pose.position.x
		self.currPosY = poseMsg.pose.pose.position.y
		self.currPosZ = poseMsg.pose.pose.position.z
		self.currOrX = poseMsg.pose.pose.orientation.x
		self.currOrY = poseMsg.pose.pose.orientation.y
		self.currOrZ = poseMsg.pose.pose.orientation.z
		self.currOrW = poseMsg.pose.pose.orientation.w

		quaternion = (
		poseMsg.pose.pose.orientation.x,
		poseMsg.pose.pose.orientation.y,
		poseMsg.pose.pose.orientation.z,
		poseMsg.pose.pose.orientation.w)

		euler = tf.transformations.euler_from_quaternion(quaternion)
		self.roll = euler[0]
		self.pitch = euler[1]
		self.yaw = euler[2]

		  

	'''def rotate_to_ball(self):
		goal=MoveBaseGoal()
		goal.target_pose.header.frame_id = "/base_link"
		goal.target_pose.pose.position.x = 0
		goal.target_pose.pose.position.y = 0
		goal.target_pose.pose.position.z = 0
		q = tf.transformations.quaternion_from_euler(0,0,self.bearingToball)
		goal.target_pose.pose.orientation.x = q[0]
		goal.target_pose.pose.orientation.y = q[1]
		goal.target_pose.pose.orientation.z = q[2]
		goal.target_pose.pose.orientation.w = q[3] 

		self.client.send_goal(goal)
		wait = self.client.wait_for_result()
		self.go_forward()'''
	
	def rotate_to_ball_2(self):
		print("Rotating as BEARING.....")		

		if(self.bearingToartag>0):
			self.twist.angular.z=0.4

		if(self.bearingToartag<0):
			self.twist.angular.z=-0.4
		self.Pub.publish(self.twist)
		time.sleep(1)
		
					  
		self.Pub.publish(self.twist)
  
	   
	def go_forward(self):
		print("I am a barbie girl, let's go party with TWIST!!")
		self.twist = Twist()
		self.twist.linear.x =0.4
		self.Pub.publish(self.twist)
		#time.sleep(3)
		print("twist ends")


	def go_forward_for3(self):
		print("I am a barbie girl, let's go party!!! with MOVEBASE :(")
		goal=MoveBaseGoal()
		goal.target_pose.header.frame_id = "/base_link"
		dist=7
		goal.target_pose.pose.position.x = dist
		goal.target_pose.pose.position.y =0
		goal.target_pose.pose.position.z = 0

		q = tf.transformations.quaternion_from_euler(0,0,0)
		goal.target_pose.pose.orientation.x = q[0]
		goal.target_pose.pose.orientation.y = q[1]
		goal.target_pose.pose.orientation.z = q[2]
		goal.target_pose.pose.orientation.w = q[3] 

		self.client.send_goal(goal)
		wait = self.client.wait_for_result()
		print("Move base ends")
		#self.count += 1
	

if __name__ == '__main__':
	try:
		Approacher()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")


