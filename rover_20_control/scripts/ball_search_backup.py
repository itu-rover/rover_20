#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2018 URC  ball searcher node starts when  arrives gps waypoint and could not detect ball 
# bearing_to_ball  topic is a string that gives ball  angle from rover. 
# first, rover is rotating  360 degree . Later it starts to search ball with sending move base goals
# ITU Rover Team
import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped,Twist
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from rover20_state_mach.msg import RoverStateMsg
import tf
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math


class GoForwardAvoid():
	def __init__(self):
		rospy.init_node('ball_search', anonymous=False)

		self.rotate_once=1
		self.send_once = 1

		self.dist=1
		self.state=RoverStateMsg()
		self.go_back_counter=0
		self.firstPosX=0
		self.firstPosY=0

		self.counter = 2
		self.point = 0
		self.twist = Twist()

		self.yaw_filter = 0
		self.counter =4

		count = 0

		
		#tell the action client that we want to spin a thread by default
		#self.Pub = rospy.Publisher('rover_navigation/cmd_vel', Twist, queue_size=10)
		rospy.Subscriber("/imu/data", Imu, self.imu_callback)
		rospy.Subscriber('/rover_state_topic',RoverStateMsg, self.stateSubscriber)
		self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #Publish Nav Goal to ROS topic

		listener = tf.TransformListener()
			
		rate = rospy.Rate(10) # 1hz
		self.state.state=self.state.FIND_IMAGE

		while not rospy.is_shutdown():
			

			#rospy.Subscriber('/move_base/result',MoveBaseActionResult, self.moveSubscriber)
			#print(self.state.state)
			
			if(self.state.state==self.state.FIND_IMAGE):
				self.send_once = 1

				
				if(count ==1):
					count = 0
					print("Now ball_search's turn !!!")

				if( self.rotate_once==1):
					print("Searching")
					self.rotate_manuel()

					self.rotate_once=0

					
				self.stroll()
		

			else:
				if(count == 0):
					count = 1
					print("waiting for state FIND_IMAGE")
			
			rate.sleep()

	def stroll(self):
		first_time = rospy.Time.now()
		count_x = 0
		rt = rospy.Rate(5)
		local_yaw = yaw
		local_yaw += math.pi

		

		self.twist.linear.x = 0.2
		self.twist.angular.z = 0.3

		while(count_x<300 and not rospy.is_shutdown()):
			if local_yaw > math.pi:
				local_yaw -= math.pi*2
			if local_yaw < -math.pi:
				local_yaw += math.pi*2

			yaw_distance = local_yaw - yaw
			print("local_yaw: "+str(local_yaw)+" yaw: "+str(yaw))
			
			if(yaw_distance > math.pi):
				yaw_distance = math.pi*2 - yaw_distance

			if(yaw_distance < -math.pi):
				yaw_distance = math.pi*2 + yaw_distance

			print("yaw_distance: "+ str(yaw_distance))
			if(yaw_distance < math.pi/20 and yaw_distance>-math.pi/20):
				self.twist.linear.x += 0.2
				local_yaw += math.pi

			last_time = rospy.Time.now()
			dt = (first_time - last_time).to_sec()
			

			self.Pub.publish(self.twist)
			count_x += 1
			rt.sleep()

	def imu_callback(self, data) :   #calculates average of 5 consecutive yaw angle data

		global roll, pitch, yaw
		yaw_for_filter = 0
		orientation_q = data.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(roll, pitch, yaw_for_filter) = euler_from_quaternion(orientation_list)     #yaw is between -pi and pi.

		#print("yaw: "+str(yaw))
		#yaw_for_filter +=  math.pi/2 #((self.imu_offset-90)/90)*math.pi

		if yaw_for_filter > math.pi:
			yaw_for_filter -= math.pi*2
		if yaw_for_filter < -math.pi:
			yaw_for_filter += math.pi*2

		self.yaw_filter += yaw_for_filter
		self.counter += 1

		if(self.counter == 5):
			yaw = self.yaw_filter/5
			self.counter = 0
			self.yaw_filter = 0


		

	
	def stateSubscriber(self,stateMsg):
		self.state=stateMsg
		if(self.state.state==self.state.REACH_IMAGE):
			if(self.send_once==1):

				print("found image")

				
				self.twist.linear.x=0
				self.twist.angular.z=0
				#self.Pub.publish(self.twist)
				self.send_once=0

		if(self.state.state == self.state.DEINITIALISE):
			self.counter = 2   #when the rover find the ball and reach it, this will 



	def rotate_manuel(self): 
		print("Rotating...")
		self.twist.linear.x = 0
		self.twist.angular.z = 0.2
		rt = rospy.Rate(5)
		count_x = 0

		while(count_x<20):
			self.Pub.publish(self.twist)
			count_x += 1
			rt.sleep()

   
	
if __name__ == '__main__':
	try:
		GoForwardAvoid()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")