#!/usr/bin/env python
# -- coding: utf-8 --
"""
----------
| NOTES  |
----------
Th hesabi yapilacak!!

WIP = Work in Progress
"""

import math
from math import sin, cos, pi, sqrt, pow
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from std_msgs.msg import String
from sensor_msgs.msg import Imu, JointState
from tf.transformations import euler_from_quaternion, quaternion_from_euler

class Localization(object):
	def __init__(self):
		rospy.init_node('odom_publisher')

		self.x = 0.0
		self.y = 0.0
		self.z = 0.0
		self.th = 0.0
		self.front_left = 0.0
		self.front_right = 0.0
		self.back_right = 0.0
		self.v = 0.0
		self.vx = 0.0
		self.vy = 0.0
		self.vth = 0.0
		self.left_wheel = 0.0
		self.right_wheel= 0.0
		self.dist_btw_wheels = 0.85 #0.85 for rover // 0.55 for husky
		self.surrounding_of_wheel = 0.155 * math.pi * 2 #0.155 for rover // 0.165 for husky
		self.reduction = 100
		self.alpha = 45.072 * math.pi / 180
		self.beta = math.pi / 2 - self.alpha
		self.counter = 0
		self.init_yaw = 0
		self.last_yaw = 0
		self.curr_yaw = 0
		self.yaw_change = 0
		self.yaw_counter = 0
		self.front_left = 0
		self.back_left = 0
		self.front_right = 0
		self.back_right = 0
		self.frequency = 10
		self.encoder_data = ""
		self.flag = 0

		self.current_time =  rospy.Time.now()
		self.last_time =  rospy.Time.now()
		self.odom_cur = Odometry()
		self.odom_pub = rospy.Publisher('/odometry/wheel', Odometry, queue_size = 10)
		rospy.Subscriber('/rover_serial_encoder', String, self.serial_callback)
		rospy.Subscriber('/imu/data', Imu, self.imu_cb)
		
		self.controller()
	
	def imu_cb(self, data):
		self.last_yaw = self.curr_yaw
		[self.curr_roll, self.curr_pitch, self.curr_yaw] = euler_from_quaternion([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]) #Convert quaternion to euler angles

		if (self.flag == 0) and self.yaw_counter < 5:
			self.yaw_counter += 1
			self.init_yaw += self.curr_yaw
			if self.yaw_counter == 5:
				self.init_yaw /= 5
				self.init_yaw += math.pi / 2
				self.flag = 1
		else:
			self.curr_yaw += math.pi / 2
			self.yaw_change = self.curr_yaw - self.last_yaw
		
	#for velocity
	def serial_callback(self,data):
		self.encoder_data = data.data
		self.splitted = data.data.split(',')

		if(self.splitted[0] == 'A'):
			if(float(self.splitted[1]) >= 1000):
				self.front_left = (-(float(self.splitted[1])-1000)) / 60
			if(float(self.splitted[1]) < 1000):
				self.front_left = (float(self.splitted[1])) / 60

			if(float(self.splitted[2]) >= 1000):
				self.back_left = (-(float(self.splitted[2])-1000)) / 60
			if(float(self.splitted[2]) < 1000):
				self.back_left = (float(self.splitted[2])) / 60

			if(float(self.splitted[3]) >= 1000):
				self.front_right = (-(float(self.splitted[3])-1000)) / 60
			if(float(self.splitted[3]) < 1000):
				self.front_right = (float(self.splitted[3])) / 60

			if(float(self.splitted[4]) >= 1000):
				self.back_right = (-(float(self.splitted[4])-1000)) / 60
			if(float(self.splitted[4]) < 1000):
				self.back_right = (float(self.splitted[4])) / 60 #saniyede alinan mesafe			

			#print(str(self.front_left) + "," + str(self.back_left) + "," + str(self.front_right) + "," + str(self.back_right))

	def controller(self):

		rate = rospy.Rate(self.frequency) #10 Hz

		while not rospy.is_shutdown():

			changed = False
			self.current_time = rospy.Time.now()
			self.dt = (self.current_time - self.last_time).to_sec()
			self.last_time = self.current_time

			self.right_wheel = ((self.front_right + self.back_right) / 2)
			self.left_wheel = ((self.front_left + self.back_left) / 2)

			self.vx = ((self.right_wheel + self.left_wheel) / 2)
			self.vy = 0
			self.vth = ((self.right_wheel - self.left_wheel) / self.dist_btw_wheels)
			
			if(self.encoder_data == ""):
				self.vx = 0
				self.vth = 0

			#Yaw change
			if self.vth < 0:
				direction = 1 #right
				self.delta_th = abs(self.vth) * self.dt * -1
			else:
				direction = 0 #left
				self.delta_th = abs(self.vth) * self.dt

			self.th += self.delta_th

			#Position change
			self.delta_x = (self.vx * cos(self.curr_yaw - self.init_yaw) * self.dt)
			self.delta_y = (self.vx * sin(self.curr_yaw - self.init_yaw) * self.dt)

			if abs(self.right_wheel - self.left_wheel) > 5:
				self.delta_x *= (1 - sin((math.pi + self.yaw_change - 2 * self.beta) / 2))
				self.delta_y *= (1 - cos((math.pi + self.yaw_change - 2 * self.beta) / 2))
				changed = True
			
			#Coordinate change
			self.x += self.delta_x
			self.y += self.delta_y
			
			print(str(self.x) + ", " + str(self.y) + ", " + str(self.front_right) + ", " + str(self.back_right))

			#Odometry message is created with calculated parameters
			self.q = tf.transformations.quaternion_from_euler(0, 0, (self.curr_yaw - self.init_yaw))
			self.odom = Odometry()
			self.odom.header.stamp = self.current_time
			self.odom.header.frame_id = "odom"
			self.odom.pose.pose = Pose(Point(self.x, self.y, self.z), Quaternion(*self.q))
			self.odom.child_frame_id = "base_link"
			self.odom.twist.twist = Twist(Vector3(self.vx, self.vy, 0), Vector3(0, 0, self.vth))
			#print(self.odom)

			self.odom_pub.publish(self.odom)
			self.encoder_data = ""

			rate.sleep()

if __name__ == '__main__':
	Localization()
