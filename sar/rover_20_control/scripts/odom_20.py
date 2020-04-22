#!/usr/bin/env python
# -*- coding: utf-8 -*-

#FREKANSA BOLUNECEK UNUTMA
#INITIAL IMU DEGERI self.th DEGERINE ATANACAK
#IMUNUN ARTIS YONUNE GORE VTH DEGERININ ARTISI BELIRLENECEK

import math
from math import sin, cos, pi, sqrt, pow
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
from std_msgs.msg import String

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
		self.dist_btw_wheels = 0.5708
		self.surrounding_of_wheel = 0.9
		self.counter = 0
		self.front_left = 0
		self.back_left = 0
		self.front_right = 0
		self.back_right = 0
		self.frequency = 10
		self.encoder_data = ""

		self.current_time =  rospy.Time.now()
		self.last_time =  rospy.Time.now()
		self.odom_cur = Odometry()
		self.odom_pub = rospy.Publisher('/odometry/wheel', Odometry, queue_size = 10)
		#self.odom_pub = rospy.Publisher('/husky_velocity_controller/odom', Odometry, queue_size = 10)
		rospy.Subscriber('/rover_serial_topic', String, self.callback)
		#rospy.Subscriber('/husky_velocity_controller/cmd_vel', Twist, self.callback)
		self.controller()
	
	#for velocity
	def callback(self,data):
		self.splitted = data.data.split(',')

		if(self.splitted[0] == 'A'):
			if(float(self.splitted[1]) >= 1000):
				self.front_left = (-(float(self.splitted[1])-1000)) * self.surrounding_of_wheel / 60
			if(float(self.splitted[1]) < 1000):
				self.front_left = (float(self.splitted[1])) * self.surrounding_of_wheel / 60

			if(float(self.splitted[2]) >= 1000):
				self.back_left = (-(float(self.splitted[2])-1000)) * self.surrounding_of_wheel / 60
			if(float(self.splitted[2]) < 1000):
				self.back_left = (float(self.splitted[2])) * self.surrounding_of_wheel / 60

			if(float(self.splitted[3]) >= 1000):
				self.front_right = (-(float(self.splitted[3])-1000)) * self.surrounding_of_wheel / 60
			if(float(self.splitted[3]) < 1000):
				self.front_right = (float(self.splitted[3])) * self.surrounding_of_wheel / 60

			if(float(self.splitted[4]) >= 1000):
				self.back_right = (-(float(self.splitted[4])-1000)) * self.surrounding_of_wheel / 60
			if(float(self.splitted[4]) < 1000):
				self.back_right = (float(self.splitted[4])) * self.surrounding_of_wheel / 60 #saniyede alinan mesafe

			self.encoder_data = "x"

			#print(str(self.front_left) + "," + str(self.back_left) + "," + str(self.front_right) + "," + str(self.back_right))

	def controller(self):

		rate = rospy.Rate(self.frequency) #10 Hz

		while not rospy.is_shutdown():

			self.current_time = rospy.Time.now()
			self.dt = (self.current_time - self.last_time).to_sec()
			self.last_time = self.current_time

			if(self.encoder_data == ""):
				self.v = 0
				self.vth = 0
			else:
				self.right_wheel = ((self.front_right + self.back_right) / 2)
				self.left_wheel = ((self.front_left + self.back_left) / 2)

				self.v = ((self.right_wheel + self.left_wheel) / 2)
				self.vth = ((self.right_wheel - self.left_wheel) / self.dist_btw_wheels)

			#self.v *= 0.09 #BUNE
			#self.vth *= 0.09 #BUNE

			self.delta_x = self.v * cos(self.th) * self.dt
			self.delta_y = self.v * sin(self.th) * self.dt
			self.delta_th = self.vth * self.dt
			self.vx = self.v * cos(self.th)
			self.vy = self.v * sin(self.th)
			self.x += self.delta_x
			self.y += self.delta_y
			self.th += self.delta_th
			
			print("v: " + str(self.v) + " , vth: " + str(self.vth) + " , th: " + str(self.th) + " , x:{} y:{}".format(self.x, self.y))
			#print("delta_x: "+ str(self.delta_x)+" , delta_y: "+str(self.delta_y)+ " , delta_th: "+ str(self.delta_th))

			#print('distance: '+str(sqrt(pow(self.x,2)+pow(self.y,2)))+'yaw: '+str(self.th)+'v:'+str(self.v)+'vth:'+str(self.vth))
			self.q = tf.transformations.quaternion_from_euler(0, 0, self.th)
			# next, we'll publish the odometry message over ROS
			self.odom = Odometry()
			self.odom.header.stamp = self.current_time
			self.odom.header.frame_id = "odom"
			# set the position
			self.odom.pose.pose = Pose(Point(self.x, self.y, self.z), Quaternion(*self.q))
			self.odom.child_frame_id = "base_link"
			
			self.odom.twist.twist = Twist(Vector3(self.vx, self.vy, 0), Vector3(0, 0, self.vth))
			# Publisher(s) 
			#print(self.odom)

			self.odom_pub.publish(self.odom)
			self.encoder_data = ""

			rate.sleep()

if __name__ == '__main__':
	Localization()