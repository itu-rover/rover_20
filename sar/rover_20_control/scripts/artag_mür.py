#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped,Twist, Point
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from rover20_state_mach.msg import StateMsg
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion
import tf
import time

x= 0.0
y= 0.0
theta = 0.0
#Servocamera = Servocamera()
# Changes are made by Berke Algul and in 24.12.2019
# Changes are made by Berke Algul and Murruvet Bozkurt in 7.2.2020

class GoForwardAvoid():
	def __init__(self):
		rospy.init_node('ball_search', anonymous=False)
		self.currPosX=0
		self.currPosY=0
		self.currPosZ=0
		self.yaw=0
		self.startMsg = "s10f"
		self.stopMsg = "s01f"
		self.resetMsg = "s00f"
		self.rotate_once=1 # deleted in code
		 # if servo completed its rotation this will be true
		self.send_once=1
		self.R=0.5
		self.ball_is_found=0
		self.dir = 1
		self.sangle = 0 #servo angle
		self.sc = 4
		self.left = False  #left artag
		self.right = False #right artag
		self.rotate_done = None
		self.half_rotate = False
		self.clockwise = None 
		self.speed = 0
		self.approach_counter = 0
		self.state=StateMsg()
		self.search_done = False
		self.counter_saw =0
		#self.imuAngle = 0
		#self.donedone = Servocamera.done_servo_rotation()
		print("waiting move base client...")
		self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		self.client.wait_for_server()
		print("client is on")
		rate = rospy.Rate(10) # 1hz
		self.search_topic = '/artag_search_done'
		#tell the action client that we want to spin a thread by default
		self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
		self.Servo_pub = rospy.Publisher('/servo_control', String, queue_size=10)
		self.done_pub = rospy.Publisher('/artag_search_done', String, queue_size=10)
		self.rover_rotated = False
		self.servo_rotating = False
		self.servo_rotated = False
		self.servo_rotation_count = 0

		while not rospy.is_shutdown():
			rospy.Subscriber('/outdoor_waypoint_nav/odometry/filtered',Odometry, self.robotPoseSubscriber)
			rospy.Subscriber('/imu/data', Imu, self.robotPoseSubscriber)
			rospy.Subscriber('/rover_state_topic',StateMsg, self.stateSubscriber)
			#rospy.Subscriber('/stage_counter_topic', String, self.stageSubscriber)
			rospy.Subscriber('/servo_angle', String, self.angleSubscriber) 
			#rospy.Subscriber('/odometry/filtered', Odometry, self.odomSubsriber)
			#print(self.state.state)
			#print("rotate_done:",  self.rotate_done)
			#print("SC: ", self.sc)
			#rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.moveSubscriber)
			#print(self.state.state)
			if (self.state.state==self.state.FIND_ARTAG):
				rospy.Subscriber('/px_coordinates', String, self.artag_Subscriber)
				rospy.Subscriber('/px_coordinates1', String, self.artag_Subscriber1)
				rospy.Subscriber('/servodone', String, self.done_rotate_Subscriber)

				#print("searching")
				print("L: ", self.left, " R: ", self.right)
				print("stage counter:", self.sc)
				#print("servo_rotated: ", self.servo_rotated)
				print("servo rotating: ", self.servo_rotating)
				print("servo_rotation_count: ", self.servo_rotation_count)
				if(self.left == True or self.right == True):
					self.counter_saw += 1

				if self.servo_rotating == False:
					print("SERVO ROTATING: FALSEEEEEE")
					if self.servo_rotation_count == 0:
						if(self.left == False and self.right == False and self.counter_saw > 0):
							self.start_servo_rotation()
							self.servo_rotating = True
							print("BURALAR DUTLUUUUK")
							continue

					if self.rover_rotated == False and self.servo_rotation_count == 1 and self.left == False and self.right == False:  
						self.clockwise = False          
						self.rotate(180)
						time.sleep(3)
						self.servo_rotated = False
						self.rover_rotated = True
						print("rover rotated")
						if(self.servo_rotated == False and self.rover_rotated == True):
							if(self.left == False and self.right == False and self.counter_saw > 0):
								self.start_servo_rotation()
								time.sleep(5)
								continue
						
					if(self.rover_rotated == True and self.servo_rotation_count == 2):
						print("Left:", self.left)
						print("Right:", self.right)
						print("SC:", self.sc)
						#print("jnbxfjbnfxjbmnbjnbjxnbjxfnbkxjnb jfnbjkfnbkjnbkjcvnbjcnbkjbnkcnbkcngbkdghbkjdnbfhnmvnbjkghjfcnbfjkfhgbfjvb gjdgbhdjkdvbngdjmvnbgdjmvdb mvfsmycebntjtghekjgtnbwtkxfwnbwdjkwhnbw jtmxvcn btwjcmtnbw tjcwvnb tjwdnhtjkbw nvcwtwtwttery")
						if(self.left == False and self.right == False):
							print("SALYANGOZ----------SALYANGOZ------------SALYANGOZ------------SALYANGOZ")
							self.go_forward()
							self.clockwise = False
							self.rotate(90)
						self.rover_rotated = False
						self.servo_rotated = False
						
					if(self.sc >= 4 and self.left == True and self.right == False):
						print("LEEFFFTTT ------- LEFTT ----------LEEFFFTTT ---------LEEFFFTTT")
						self.speed = 2
						self.go_forward()
						time.sleep(4)
						self.client.cancel_goal()
						self.clockwise = True
						self.rotate(90)
						time.sleep(3)
						self.speed = 2 
						self.go_forward() 
						time.sleep(4)
						self.client.cancel_goal()
						self.clockwise = False  
						self.rotate(90)
						time.sleep(3)


					if(self.sc >= 4 and self.right == True and self.left == False):
						print("RIGHTTTT ------- RIGHTTTT ------------- RIGHTTTT---------RIGHTT")
						self.speed = 2
						self.go_forward()
						time.sleep(4)
						self.client.cancel_goal()
						#self.client.cancel_all_goals()
						self.clockwise = False 
						self.rotate(90)
						time.sleep(3)
						self.speed = 2
						self.go_forward()
						time.sleep(4)
						self.client.cancel_goal()
						self.clockwise = True
						self.rotate(90)
						time.sleep(3)

						
			if self.search_done == True:
				self.done_pub.publish("1")
			else:
				self.done_pub.publish("0")			

			rate.sleep()

	def imuSubscriber(self, msg):
		q = msg.pose.orientation.z
		e = euler_from_quaternion(q)
		self.imuAngle = e[2]

	def stateSubscriber(self,stateMsg):
		self.state=stateMsg
		if(self.state.state==self.state.REACH_ARTAG or self.state.state==self.state.APPROACH):# and self.approach_counter > 0): # LET MUR KNOW THIS -Berke Algül
			if(self.send_once==1):
				self.search_done = True
				print("SEARCH DONE:", self.search_done)
				print("found artag")
				#print("APPROACH_COUNTER:", self.approach_counter)
				self.stop_servo_rotation() #stop servo
				time.sleep(2)				
				rospy.Subscriber('/servo_angle', String, self.angleSubscriber) #subscribe servo angle
				try:
					sangleStr = self.sangle[:3]
					self.sangle = int(float(sangleStr))
				except:
					print("Error: ",sangleStr)

				print("ANGLE OF SERVO CAMERA: ", self.sangle)
				time.sleep(2)# DELAY REDUCED
				self.servoangle2 = (self.yaw - int(float(self.sangle)))
				if(self.servoangle2 < 0):
					self.clockwise = False
				if(self.servoangle2 > 0):
					self.clockwise = True
				#self.servoangle2 = 360 + int(float(self.servoangle))
				print("YAWWWWWWWW", self.yaw)
				print("Rotate angle : ", self.servoangle2)
				self.rotate(abs(self.servoangle2)) #Rover turns as much as the angle the servo sees the artag.
				time.sleep(5)
				self.twist = Twist()
				self.twist.linear.x=0
				self.twist.angular.z=0
				self.Pub.publish(self.twist)
				#self.client.cancel_goal()
				#self.client.cancel_all_goals()
				self.send_once=0
				self.half_rotate = True
				if(self.half_rotate == True):
					print("we are here, baby!!")
					self.Servo_pub.publish(self.resetMsg)


	def angleSubscriber(self, data): 
		self.sangle = data.data #convert string to integer.

	def stageSubscriber(self, data): #px_coordinates
		self.sc = data.data
		#print("stage:", self.sc/home/muruvvet/rover20_ws/src/rover_20/rover_20_control/scripts/artag_search.py)

	def artag_Subscriber(self, data): #px_coordinates1
		self.a_coor = data.data

		if self.a_coor != "-":
			self.left = True
		else:
			self.left = False

	def artag_Subscriber1(self, data):
		self.a_coor1 = data.data

		if self.a_coor1 != "-":
			self.right = True
		else:
			self.right = False

	def done_rotate_Subscriber(self, data):
		self.rotate_done = data.data
		#print("lkdsfjfkh")
		if(self.rotate_done == "1" and self.servo_rotating == True):
			print("rotate_done is true")
			self.servo_rotating = False
			self.servo_rotation_count += 1
		'''else:
			self.servo_rotated = False'''
		
	def robotPoseSubscriber(self,poseMsg): #Odometry update recieved from ROS topic, run this function
		quaternion = (
		poseMsg.orientation.x,
		poseMsg.orientation.y,
		poseMsg.orientation.z,
		poseMsg.orientation.w)
		euler = tf.transformations.euler_from_quaternion(quaternion)
		self.roll = euler[0]
		self.pitch = euler[1]
		self.yaw = euler[2]

	def go_forward(self):
		print("Going forward...")
		goal=MoveBaseGoal()
		goal.target_pose.header.frame_id = "/base_link"
		dist=1                                                #1 metre ileri gidiyor 
		goal.target_pose.pose.position.x = dist
		goal.target_pose.pose.position.y =0
		goal.target_pose.pose.position.z = 0

		q = tf.transformations.quaternion_from_euler(0,0,0)
		goal.target_pose.pose.orientation.x = q[0]
		goal.target_pose.pose.orientation.y = q[1]
		goal.target_pose.pose.orientation.z = q[2]
		goal.target_pose.pose.orientation.w = q[3]

		self.client.send_goal(goal)
		#wait = self.client.wait_for_result()
		print("-------------------MOVE BASE ENDS.------------")

	'''def go_forward(self):
		print("I am a barbie girl, let's go party with TWIST!!")
		self.twist = Twist()
		self.twist.linear.x =0.5 + self.speed
		self.speed += 0.2 
		print("Move base ends")'''

	def rotate(self, angle):
		print("Rotating according to servo angle...")
		angle = angle*2*pi/360
		self.twist = Twist()
		if(self.clockwise == True):
			self.twist.angular.z= -0.4
		if(self.clockwise == False):
			self.twist.angular.z = 0.4
		self.twist.linear.x=0
		self.t0 = rospy.Time.now().to_sec()
		self.current_angle = 0
		while(self.current_angle < angle):
			self.Pub.publish(self.twist)
			self.t1 = rospy.Time.now().to_sec()
			self.current_angle = 0.4*(self.t1-self.t0)
		#self.Pub.publish(self.twist)


	def start_servo_rotation(self):
		self.Servo_pub.publish(self.startMsg)
		#self.servo_rotated = False
		self.servo_rotating = True
		#self.servo_rotation_count += 1
		print("servo has started to rotate.")
		self.approach_counter += 1

	def stop_servo_rotation(self):
		self.Servo_pub.publish(self.stopMsg)
		#self.servo_rotated = True
		self.servo_rotating = False
		print("servo had stopped")
		self.servo_rotation_count = 4
		print("APPROACH_COUNTER:", self.approach_counter)


	'''def odomSubscriber(self, msg):
		global x 
		global y
		global theta

		x = msg.pose.pose.position.x 
		y = msg.pose.pose.position.y

		rotation_q = msg.pose.pose.orientation

		(roll, pitch, theta) = euler_from_quaternion([rotation_q.x, rotation_q.y, rotation_q.z, rotation_q.w])

	def go_forward(self):
		print("Going forward...")
		rospy.Subscriber('/odometry/filtered', Odometry, self.odomSubscriber)
		time.sleep(2)
		speed = Twist()
		#r = rospy.rate(4)
		goal = Point()
		dist = 0.5
		goal.x = dist
		goal.y = 0

		delta_x = goal.x - x
		delta_y = goal.y - y

		angle_of_goal = atan2(delta_y, delta_x)
		while delta_x < 0.1:
			rospy.Subscriber('/odometry/filtered', Odometry, self.odomSubscriber)
			speed.linear.x = 0.4
			speed.angular.z = 0.0
			print("let's go part!!aaaaaaa")
			delta_x = goal.x - x
			
		dist += 0.5

		self.Pub.publish(speed)'''       

if __name__ == '__main__':
	try:
		GoForwardAvoid()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")

