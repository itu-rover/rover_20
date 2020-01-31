#!/usr/bin/env python
# -- coding: utf-8 --

#EN CALİSANİMSİ ENCODER KODU BU!

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
from sensor_msgs.msg import Imu
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
		self.dist_btw_wheels = 0.42
		self.surrounding_of_wheel = 0.165 * math.pi * 2
		self.reduction = 100
		self.counter = 0
		self.curr_yaw = 0
		self.front_left = 0
		self.back_left = 0
		self.front_right = 0
		self.back_right = 0
		self.frequency = 10
		self.encoder_data = ""
		self.flag = 0
		self.yaw = 0

		self.current_time =  rospy.Time.now()
		self.last_time =  rospy.Time.now()
		self.odom_cur = Odometry()
		self.odom_pub = rospy.Publisher('/odometry/wheel', Odometry, queue_size = 10)
		#self.odom_pub = rospy.Publisher('/husky_velocity_controller/odom', Odometry, queue_size = 10)
		rospy.Subscriber('/rover_serial_topic', String, self.callback)
		rospy.Subscriber('/imu/data', Imu, self.imu_cb)
		
		#rospy.Subscriber('/husky_velocity_controller/cmd_vel', Twist, self.callback)
		self.controller()
	
	def imu_cb(self, data):
		[self.curr_roll, self.curr_pitch, curr_yaw] = euler_from_quaternion([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]) #Convert quaternion to euler angles
		yaw = 0

		#Get average of yaw measurements
		for i in range(5):
			yaw += curr_yaw
		self.curr_yaw = yaw / 5
		if (self.flag == 0):
			self.yaw = self.curr_yaw
			self.flag = 1
		
	#for velocity
	def callback(self,data):
		self.encoder_data = data.data
		self.splitted = data.data.split(',')

		if(self.splitted[0] == 'A'):
			if(float(self.splitted[1]) >= 1000):
				self.front_left = (-(float(self.splitted[1])-1000))  / 60
			if(float(self.splitted[1]) < 1000):
				self.front_left = (float(self.splitted[1]))  / 60

			if(float(self.splitted[2]) >= 1000):
				self.back_left = (-(float(self.splitted[2])-1000))  / 60
			if(float(self.splitted[2]) < 1000):
				self.back_left = (float(self.splitted[2]))  / 60

			if(float(self.splitted[3]) >= 1000):
				self.front_right = (-(float(self.splitted[3])-1000))  / 60
			if(float(self.splitted[3]) < 1000):
				self.front_right = (float(self.splitted[3]))  / 60

			if(float(self.splitted[4]) >= 1000):
				self.back_right = (-(float(self.splitted[4])-1000))  / 60
			if(float(self.splitted[4]) < 1000):
				self.back_right = (float(self.splitted[4]))  / 60 #saniyede alinan mesafe

			

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

				self.vx = ((self.right_wheel + self.left_wheel) / 2)
				self.vy = 0
				self.vth = ((self.right_wheel - self.left_wheel) / self.dist_btw_wheels)

			#self.v *= 0.09 #BUNE
			self.vth *= 0.135 #BUNE
			
			#yaw değişimi
			if self.vth < 0:
				direction = 1 #right
				self.delta_th = abs(self.vth) * self.dt * -1
			else:
				direction = 0 #left
				self.delta_th = abs(self.vth) * self.dt

			self.th += self.delta_th
			"""
			if self.th > math.pi * 2:
				self.th -= math.pi * 2
			elif self.th < -math.pi * 2:
				while(self.th < 0):
					self.th += math.pi * 2
			"""
			#if self.th < 0:
			#	self.th = math.pi - self.th

			#konum değişimi
			self.delta_x = self.vx * cos(self.th) * self.dt
			self.delta_y = self.vx * sin(self.th) * self.dt
			#self.delta_dist = math.sqrt(delta_x*delta_x + delta_y*delta_y)
			
			#koordinat değişimi
			self.x += self.delta_x
			self.y += self.delta_y
			
			#self.yaw += self.delta_th
		
			#self.vtot = math.sqrt((self.vx*self.vx) + (self.vy+self.vy))
			
			print("th: " + str(math.degrees(self.th)) + ",deltath: " + str(math.degrees(self.delta_th)))
			print("vth: " + str(self.vth))
			#print("cos: " + str(cos(self.th)) + " , sin: " + str(sin(self.th)))
			#print("vx: " + str(self.vx) + " , vy: " + str(self.vy))
			#print("dx: " + str(self.delta_x) + " , dy: " + str(self.delta_y))
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
			
			#if(self.vx == 0):
			#	self.th = 0

			rate.sleep()

if __name__ == '__main__':
	Localization()