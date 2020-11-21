#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
----------
|  TODO  |
----------

Integrate with state machine
Find yaw offset of current position
Yaw counter may be added

----------
| NOTES  |
----------

Imu is publishing yaw according to magnetic east

Go to these coordinates in playground: 41.1053, 29.0236

WIP = Work in Progress

"""

import rospy
import math
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix, Imu, LaserScan
import geopy.distance
from std_msgs.msg import String
#from rover20_state_mach.msg import RoverStateMsg
from empty_space_class import EmptySpace

class autonomous():
	def __init__(self):
		rospy.init_node("autonomous_node")

		#Movement variables
		#Basics
		self.twist = Twist()
		self.dist = 0 #Distance to target
		self.last_dist = 0
		self.encoders_working = True
		#GPS
		self.init_lat = 0
		self.init_lon = 0
		self.counter_lat = 0
		self.counter_lon = 0
		self.gps_flag = False
		self.gps_flag_counter = 0
		self.curr_lat = 0
		self.curr_lon = 0
		self.target_lat = 0
		self.target_lon = 0
		#Odom
		self.curr_x = 0
		self.curr_y = 0
		self.target_x = 0
		self.target_y = 0
		#Rotation
		self.curr_yaw = 0
		self.last_yaw = 0
		#Others
		self.goal_reach_thresh = rospy.get_param("movement/goal_reach_thresh", 1.5) #Minimum distance from goal point
		self.turn_speed = rospy.get_param("movement/turn_speed", 0.8) #Rotate speed on z axis
		self.yaw_turn_rate_max = rospy.get_param("movement/yaw_turn_rate_max", 15) #Number of iterations needed to turn to target yaw
		self.yaw_turn_rate_min = rospy.get_param("movement/yaw_turn_rate_min", 10)
		self.yaw_turn_rate = self.yaw_turn_rate_max
		self.yaw_angle_error_divider = rospy.get_param("movement/yaw_angle_error_divider", 30) #Yaw error while turning to target
		self.yaw_angle_error = math.pi / self.yaw_angle_error_divider
		self.yaw_offset = 0 #math.pi / 2 #Yaw offset of rover default: magnetic east
		self.fix_yaw_on_cb = True

		#Wheel parameters
		self.wheel_radius = rospy.get_param("vehicle/wheel/radius", 0.15) #Radius of wheel
		self.wheel_surrounding = 2 * math.pi * self.wheel_radius #Surrounding of wheel
		self.wheel_reduction = rospy.get_param("vehicle/wheel/reduction", 500) #Reduction rate of wheel motor
		self.body_width = rospy.get_param("vehicle/body/width", 1) #Width of vehicle with wheels
		self.body_length = rospy.get_param("vehicle/body/length", 1) #Length of vehicle with wheels
		self.wheel_dist = rospy.get_param("vehicle/wheel/dist", 1) #Distance between wheels

		#Lidar variables
		self.lidar_angle = rospy.get_param("lidar/lidar_angle", 15) #Scan range from 0 -> front of the rover
		self.lidar_scan_angle = math.pi * self.lidar_angle / 180 #Scan range in radians
		self.latest_scan = None #Latest lidar scan data
		self.lidar_angle_min = rospy.get_param("lidar/lidar_min_scan_angle", -135) * math.pi / 180 #Minimum range of lidar to scan
		self.lidar_angle_max = rospy.get_param("lidar/lidar_max_scan_angle", 135) * math.pi / 180 #Maximum range of lidar to scan
		self.lidar_angle_increment = math.pi / rospy.get_param("lidar/lidar_angle_increment", 314.16)
		self.lidar_range_min = int(((self.lidar_angle_max - self.lidar_angle_min) / 2 - self.lidar_scan_angle) / self.lidar_angle_increment) #Minimum angle to detect obstacle
		self.lidar_range_max = int(((self.lidar_angle_max - self.lidar_angle_min) / 2 + self.lidar_scan_angle) / self.lidar_angle_increment) #Maximum angle to detect obstacle
		self.lidar_range_average = (self.lidar_range_min + self.lidar_range_max) / 2 #Middle of scan ranges
		self.lidar_obstacle_range = rospy.get_param("lidar/obstacle_range", 3.0) #Range to detect object

		#Empty space parameters
		self.min_empty_space_points = rospy.get_param("empty_spaces/empty_space_points", 10) #Minimum empty space points to take it as empty
		self.print_empty_spaces = rospy.get_param("empty_spaces/print_empty_spaces", True) #If True, prints empty spaces found
		self.turn_to_empty_space = rospy.get_param("empty_spaces/turn_to_space", True) #If True, rotate through empty space available
		self.empty_space_min_angle = rospy.get_param("empty_spaces/min_angle", -90) * math.pi / 180 #Minimum angle to check for empty space tracking
		self.empty_space_max_angle = rospy.get_param("empty_spaces/max_angle", 90) * math.pi / 180 #Maximum angle to check for empty space tracking
		self.empty_space_range_min = int(((self.lidar_angle_max - self.lidar_angle_min) / 2 + self.empty_space_min_angle) / self.lidar_angle_increment) #Minimum angle to detect empty space
		self.empty_space_range_max = int(((self.lidar_angle_max - self.lidar_angle_min) / 2 + self.empty_space_max_angle) / self.lidar_angle_increment) #Maximum angle to detect empty space
		self.empty_space_noise_tolerance = rospy.get_param("empty_spaces/empty_space_noise_tolerance", 2) #Maximum number of points that can be seen due to noise
		self.empty_space_pass_tolerance = rospy.get_param("empty_spaces/empty_space_pass_tolerance", 0.2) #Distance tolerance while passing from empty space

		#Publisher and subscriber topics
		self.twist_pub_topic = rospy.get_param("topics/twist_pub_topic", "/cmd_vel")
		self.serial_pub_topic = rospy.get_param("topics/serial_pub_topic", "/rover_serial_topic")
		self.odom_sub_topic = rospy.get_param("topics/odom_sub_topic", "/odometry/filtered_map")
		self.lidar_sub_topic = rospy.get_param("topics/lidar_sub_topic", "/scan")
		self.encoder_sub_topic = rospy.get_param("topics/encoder_sub_topic", "/rover_serial_encoder")
		self.gps_sub_topic = rospy.get_param("topics/gps_sub_topic", "/gps/fix")

		#Publisher and subscriber definitions
		self.twist_pub = rospy.Publisher(self.twist_pub_topic, Twist, queue_size = 50)

		rospy.Subscriber(self.lidar_sub_topic, LaserScan, self.lidar_cb)
		rospy.Subscriber(self.odom_sub_topic, Odometry, self.odom_cb)
		rospy.Subscriber(self.gps_sub_topic, NavSatFix, self.gps_cb)
		
		#Initialising commands
		self.reset_twist()
		#self.manual_input()
		self.autonomous_drive()

	def check_yaw_change(self):
		if abs(self.curr_yaw - self.last_yaw) > 0.1:
			return True
		else:
			return False

	def lidar_cb(self, data):
		self.latest_scan = data
	
	def odom_cb(self, data):
		self.latest_odom = data
		self.curr_x = data.pose.pose.position.x #* -1
		self.curr_y = data.pose.pose.position.y #* -1

		self.curr_roll, self.curr_pitch, self.curr_yaw = euler_from_quaternion([data.pose.pose.orientation.x, data.pose.pose.orientation.y, data.pose.pose.orientation.z, data.pose.pose.orientation.w]) #Convert quaternion to euler angles
		self.curr_yaw += self.yaw_offset

		if self.fix_yaw_on_cb:
			self.curr_yaw = self.fix_yaw_angle(self.curr_yaw)

		#print(self.curr_yaw)

	def gps_cb(self, data):
		if self.gps_flag:
			self.curr_lat = data.latitude
			self.curr_lon = data.longitude
		elif (not self.gps_flag) and self.gps_flag_counter != 5:
			self.counter_lon += data.longitude
			self.counter_lat += data.latitude
			self.gps_flag_counter += 1
		elif self.gps_flag_counter == 5:
			self.init_lat = self.counter_lat / 5
			self.init_lon = self.counter_lon / 5
			self.gps_flag = True

	def gps_to_xy(self):
		self.target_y = float(1000 * geopy.distance.VincentyDistance((self.init_lat, 0), (self.target_lat, 0)).km)
		self.target_x = float(1000 * geopy.distance.VincentyDistance((0, self.init_lon), (0, self.target_lon)).km)

	#Find density of objects in scan range
	def find_obstacle_density(self, data = None):
		left_density = 0
		right_density = 0

		if data is None:
			data = self.latest_scan

		#Check all scan ranges
		for i in range(self.lidar_range_min, self.lidar_range_max):
			#Find real distance
			if i < self.lidar_range_average:
				curr_angle = abs(self.lidar_range_average - i) * self.lidar_angle_increment
			else:
				curr_angle = abs(i - self.lidar_range_average) * self.lidar_angle_increment

			obstacle_range = int(self.lidar_obstacle_range) / math.cos(curr_angle)

			#If there are any obstacle in range, increase related side's number
			if data.ranges[i] < obstacle_range:
				if i < self.lidar_range_average:
					left_density += 1
				else:
					right_density += 1

		#Return true if left side's obstacle density is bigger
		if left_density > right_density:
			return True
		else:
			return False

	#Find empty spaces from latest scan
	def find_empty_spaces(self, data = None):
		empty_spaces = [] #List to put empty spaces in current scan
		
		if data is None:
			data = self.latest_scan

		inf_iters = 0 #Number of inf values
		iter_start = 0 #Start index of inf values
		iter_finish = 0 #Last index of inf value
		noise_count = 0 #Number of noise points

		#Check all scan ranges
		for i in range(self.empty_space_range_min, self.empty_space_range_max):
			if data.ranges[i] == float('Inf'): #Increase inf counter by one
				if inf_iters == 0:
					iter_start = i

				inf_iters += 1

			#Check noise count
			elif data.ranges[i] != float('Inf') and noise_count < self.empty_space_noise_tolerance:
				noise_count += 1
				inf_iters += 1

			#Check if amount of points are equal to be counted as empty space then reset start and finish points
			if (i == self.empty_space_range_max - 1) or (data.ranges[i] != float('Inf') and noise_count == self.empty_space_noise_tolerance):
				if inf_iters >= self.min_empty_space_points:
					iter_finish = i
					new_space = EmptySpace(iter_av = self.lidar_range_average, iter_start = iter_start, iter_finish = iter_finish, angle_increment = self.lidar_angle_increment)
					empty_spaces.append(new_space)

				#Reset counters
				inf_iters = 0
				iter_start = 0
				iter_finish = 0
				noise_count = 0

		#Print empty spaces if wanted
		if self.print_empty_spaces:
			for i in range(len(empty_spaces)):
				print("Empty Space {}:\n".format(i))
				if empty_spaces[i] is not None:
					empty_spaces[i].print_me()

			rospy.sleep(0.2)

		return empty_spaces

	#Find largest space from found empty space points
	def find_largest_space(self, data = None):
		if data is None:
			data = self.latest_scan

		empty_spaces = self.find_empty_spaces(data = data) #Find empty spaces from latest scan

		largest_space = None
		largest_space_width = 0

		#Check empty spaces
		for empty_space in empty_spaces:
			if empty_space.space_width > largest_space_width:
				largest_space_width = empty_space.space_width
				largest_space = empty_space

		#Rotate through center point of empty space
		if self.turn_to_empty_space and largest_space is not None:
			#Find angle between middle of empty space and our iteration start point
			angle = (((largest_space.iter_start + largest_space.iter_finish) / 2) - self.lidar_range_average) * self.lidar_angle_increment
			self.turn_to_yaw(angle, angle_error_threshold = math.pi / 30)

		return largest_space

	#https://www.youtube.com/watch?v=oCXfMJnGWaA

	#Find closest space that rover can fit
	def find_fitting_space(self, data = None):
		if data is None:
			data = self.latest_scan

		empty_spaces = self.find_empty_spaces(data = data) #Find empty spaces from latest scan

		best_space = None
		second_best_space = None		
		#Melih psp'mi aldi, uzuldum (psp arekin)
		#Check empty spaces
		for empty_space in empty_spaces:
			#Find angle between middle point of empty space and vehicle
			angle = (((empty_space.iter_start + empty_space.iter_finish) / 2) - self.lidar_range_average) * self.lidar_angle_increment
			relative_vehicle_width = self.body_length * math.sin(angle) + self.body_width * math.cos(angle) #Compute vehicle length when it turns to middle point

			#Check if empty space is 
			if relative_vehicle_width + self.empty_space_pass_tolerance < empty_space.space_width:
				if best_space is not None:
					if abs(self.lidar_range_average - empty_space.iter_start) < abs(self.lidar_range_average - best_space.iter_start):
						best_space = empty_space
					elif second_best_space is None:
						second_best_space = empty_space
					elif second_best_space is not None and abs(self.lidar_range_average - empty_space.iter_start) < abs(self.lidar_range_average - second_best_space.iter_start):
						second_best_space = empty_space
				else:
					best_space = empty_space

		#Rotate through center point of empty space
		if self.turn_to_empty_space and best_space is not None:
			#Find angle between middle of empty space and our iteration start point
			#angle = (((best_space.iter_start + best_space.iter_finish) / 2) - self.lidar_range_average) * self.lidar_angle_increment
			#self.turn_to_yaw(angle, angle_error_threshold = math.pi / 30)
			for i in range(best_space.iter_start, best_space.iter_finish):
				alpha = (i - best_space.iter_start) * best_space.angle_increment
				theta = (best_space.iter_start - self.lidar_range_average) * best_space.angle_increment
				relative_w = self.body_width * math.cos(theta + alpha / 2) + self.body_length * math.sin(theta + alpha / 2)
				x1 = self.lidar_obstacle_range / math.cos(theta - self.yaw_angle_error)
				x2 = self.lidar_obstacle_range / math.cos(theta + alpha + self.yaw_angle_error)

				if (self.empty_space_pass_tolerance + relative_w) < math.sqrt(x1 ** 2 + x2 ** 2 - 2 * x1 * x2 * math.cos(alpha + 2 * self.yaw_angle_error)):
					self.turn_to_yaw(self.curr_yaw + theta + alpha / 2)
					break
				else:
					continue

		print("Best space: ")
		if best_space is not None:
			best_space.print_me()
		else:
			print("None\n")

		return best_space

	#https://www.youtube.com/watch?v=EOCUaHm4yQA
	#Control laserscan data
	def control_laserscan(self, data = None):
		obstacle_found = False

		if data is None:
			data = self.latest_scan

		#If any obstacle is found in obstacle detection range, return True
		if data is not None:
			for i in range(self.lidar_range_min, self.lidar_range_max):
				if data.ranges[i] < self.lidar_obstacle_range:
					obstacle_found = True
					break
				else:
					obstacle_found = False

		return obstacle_found

	def reset_twist(self):
		self.twist.linear.x  = 0
		self.twist.linear.y  = 0
		self.twist.linear.z  = 0
		self.twist.angular.x = 0
		self.twist.angular.y = 0
		self.twist.angular.z = 0
		self.twist_pub.publish(self.twist)

	#Publish speed data and then reset twist
	def go_forward(self, speed, secs):
		rate = rospy.Rate(10)
		self.twist.linear.x = speed
		for i in range(int(secs * 10)):
			self.twist_pub.publish(self.twist)
			rate.sleep()
		self.reset_twist()

	#Publish rotation speed data and then reset twist
	def turn(self, speed, secs):
		rate = rospy.Rate(10)
		self.twist.angular.z = speed
		for i in range(int(secs * 10)):
			self.twist_pub.publish(self.twist)
			#print("curr_x: {}, curr_y: {}, dist: {}".format(self.curr_x, self.curr_y, self.get_dist_xy(self.target_x, self.target_y)))
			rate.sleep()
		self.reset_twist()

	#Publish speed data until reaching destination
	#XY beraber entegre edilmeli !!!!
	def go_x_meters(self, speed, meters):
		initial_dist = self.curr_x
		rate = rospy.Rate(10)
		self.twist.linear.x = speed
		while self.curr_x * abs(speed) / speed < initial_dist + meters * abs(speed) / speed:
			self.twist_pub.publish(self.twist)
			#print("curr_x: {}, curr_y: {}, init_dist: {}, dest: {} dist: {}".format(self.curr_x, self.curr_y, initial_dist, meters, self.get_dist_xy(self.target_x, self.target_y)))
			rate.sleep()
		self.reset_twist()
		#print("curr_x: {}, curr_y: {}".format(self.curr_x, self.curr_y))

	#Get distance between two points in meters
	def get_dist_xy(self, targetx, targety):
		self.last_dist = self.dist
		self.dist = float(math.sqrt(math.pow((targetx - self.curr_x), 2) + math.pow((targety - self.curr_y), 2)))
		#print("curr_x: {}, curr_y: {}, dist: {}".format(self.curr_x, self.curr_y, self.dist))
		return self.dist

	#Get distance between two coordinates in meters
	def get_dist_latlon(self, target_coords):
		self.last_dist = self.dist
		self.dist = float(1000 * geopy.distance.VincentyDistance((self.curr_lat, self.curr_lon), target_coords).km)
		print("Distance to target = {}".format(self.dist))
		return self.dist

	def turn_to_yaw(self, target_yaw, angle_error_threshold = None):
		#If no threshold is assigned, assign from configurations
		if angle_error_threshold == None:
			angle_error_threshold = self.yaw_angle_error

		print("Turning to: {}".format(target_yaw))
		#Get target yaw in [-pi, +pi] range
		target_yaw = self.fix_yaw_angle(target_yaw)
		yaw_dist = self.curr_yaw - target_yaw

		#print("curr_yaw: {}, target_yaw: {}, yaw_dist: {}".format(self.curr_yaw, target_yaw, yaw_dist))

		#If current yaw error is bigger than threshold value, continue to rotate through target yaw
		while (yaw_dist > angle_error_threshold) or (yaw_dist < -1 * angle_error_threshold):
			#print("curr_yaw: {}, target_yaw: {}, yaw_dist: {}".format(self.curr_yaw, target_yaw, yaw_dist))
			#Correct the sign of rotation
			self.turn(math.copysign(self.turn_speed, -1 * yaw_dist), 0.2)
			self.curr_yaw = self.fix_yaw_angle(self.curr_yaw)
			yaw_dist = self.curr_yaw - target_yaw

		#print("curr_yaw: {}, target_yaw: {}, yaw_dist: {}".format(self.curr_yaw, target_yaw, yaw_dist))

	#If yaw angle is not in [-pi, +pi] range, fix it
	def fix_yaw_angle(self, yaw):
		while not (yaw < math.pi and yaw > -math.pi):
			if yaw > math.pi:
				yaw -= math.pi * 2
			elif yaw < -math.pi:
				yaw += math.pi * 2
			else:
				break

		return yaw

	#https://www.youtube.com/watch?v=TXzO1FT6OVs

	def obstacle_avoidance(self, turn_sec = 1):
		#While having obstacle in front of rover, detect density of obstacles and rotate through correct way
		while self.control_laserscan():			
			#empty_space = self.find_largest_space() #Find largest space
			empty_space = self.find_fitting_space() #Find closest empty space that vehicle can fit

			if empty_space is None: #If there are no empty spaces available, use obstacle density function instead
				if self.find_obstacle_density():
					self.turn(self.turn_speed, turn_sec)
				else:
					self.turn(-1 * self.turn_speed, turn_sec)
			else:
				empty_space.print_me()

		#Check laserscan for 5 times
		for i in range(5):
			if not self.control_laserscan():
				rospy.sleep(0.2)
			else:
				print("Found obstacle")
				self.go_forward(-1, 0.5)
				return False
		return True

	#Manual control of rover
	def manual_input(self):
		while not rospy.is_shutdown():
			print("Enter mode you want F: forward, T: turn, M: go x meters")
			choose = raw_input()
			print("Enter your speed")
			speed = int(raw_input())
			print("Enter seconds / meters you want to go")
			secs = int(raw_input())
			if choose.upper() == "F":
				self.go_forward(speed, secs)			
			elif choose.upper() == "T":
				self.turn(speed, secs)
			elif choose.upper() == "M":
				self.go_x_meters(speed, secs)
			self.reset_twist()

	#Get xy input from user
	def xy_input(self):
		print("Enter XY points: ")
		self.target_x = float(raw_input()) #* -1
		self.target_y = float(raw_input())
		print("Target x: {}, Target y: {}".format(self.target_x, self.target_y))
		print("Distance to target: {}".format(self.get_dist_xy(self.target_x, self.target_y)))

	#https://www.youtube.com/watch?v=XNZKzbSA1t4

	#Get GPS input from user
	def gps_input(self):
		print("Enter GPS coordinates (latitude and longitude): ")
		self.target_lat = float(raw_input())
		self.target_lon = float(raw_input())
		self.gps_to_xy()

	#https://www.youtube.com/watch?v=e_qgUbKuhGg

	def autonomous_drive(self):
		#self.gps_input() #Get coordinates from user
		self.xy_input()

		#Find angle and turn to target
		if self.encoders_working:
			angle = math.atan2((self.target_y - self.curr_y), (self.target_x - self.curr_x))
			self.turn_to_yaw(angle)
			self.get_dist_xy(self.target_x, self.target_y)
		else:
			angle = math.atan2((self.target_lat - self.curr_lat), (self.target_lon - self.curr_lon))
			self.turn_to_yaw(angle)
			self.get_dist_latlon((self.target_lat, self.target_lon))

		for i in range(500):
			yaw_counter = 0

			if i % self.yaw_turn_rate == 0: #Turn to target every self.yaw_turn_rate iteration
				if self.encoders_working:
					angle = math.atan2((self.target_y - self.curr_y), (self.target_x - self.curr_x))
					self.turn_to_yaw(angle)
				else:
					angle = math.atan2((self.target_lat - self.curr_lat), (self.target_lon - self.curr_lon))
					self.turn_to_yaw(angle)

			if not self.control_laserscan(): #Go forward if there is no obstacle in front of rover
				if self.encoders_working:
					#self.go_x_meters(1, 1)
					self.go_forward(1, 1)
				else:
					self.go_forward(1, 1)
			else:
				if self.obstacle_avoidance(turn_sec = 0.4): #Get rid of obstacles in front, then go forward
					if self.encoders_working:
						#self.go_x_meters(1, 1)
						self.go_forward(1, 1)
					else:
						self.go_forward(1, 1)

			if self.encoders_working:
				self.dist = self.get_dist_xy(self.target_x, self.target_y)
			else:
				self.dist = self.get_dist_latlon((self.target_lat, self.target_lon))

			#Change turn rate based on distance to target point
			if self.dist > 15.0:
				self.yaw_turn_rate = self.yaw_turn_rate_min
			elif self.dist < 15.0 and self.dist > 5.0:
				self.yaw_turn_rate = self.yaw_turn_rate_max
			else:
				self.yaw_turn_rate = 5

			if self.dist > self.last_dist:
				self.yaw_turn_rate = 5

			#If rover is closer to the target less than threshold, publish goal reach message and finish
			if float(self.dist) < float(self.goal_reach_thresh):
				print("Goal reached!")
				self.reset_twist()
				break

			if self.check_yaw_change():
				yaw_counter += 1

			if yaw_counter >= 4:
				if self.encoders_working:
					angle = math.atan2((self.target_y - self.curr_y), (self.target_x - self.curr_x))
				else:
					angle = math.atan2((self.target_lat - self.curr_lat), (self.target_lon - self.curr_lon))
				self.turn_to_yaw(angle)

		self.autonomous_drive()

if __name__ == "__main__":
	autonomous()