#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
----------
| NOTES  |
----------
Imu is publishing yaw according to magnetic east
Gazebo axis' are different, should be changed if used during simulation
rotatesiz 180

WIP = Work in Progress
"""

import rospy
from nmea_msgs.msg import Sentence
import math
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from nav_msgs.msg import Odometry, Path
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import NavSatFix
import geopy.distance
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from node_classv3 import Node
import geonav_transform.geonav_conversions as gc
reload(gc)

class Autonomous():
	def __init__(self):
		rospy.init_node("autonomous_node")

		#Debug parameters
		self.lidar_used = True
		self.outdoor_drive = False
		self.debug_nodes = False

		#Movement variables
		self.twist = Twist()
		self.trail = Path()
		self.yaw = 0
		self.x = 0
		self.y = 0
		self.lat = 0
		self.lon = 0
		self.olat = 0
		self.olon = 0
		self.rviz_x = 0
		self.rviz_y = 0
		self.target_x = 0
		self.target_y = 0
		self.target_lat = 0
		self.target_lon = 0
		self.node_angle = -94.305 * math.pi / 180 #Rightest
		self.min_nodes = 3
		self.dist_threshold = 1.0
		self.dist = 0

		#Scan variables
		self.latest_scan = None
		self.empty_space_iter_start = 1
		self.empty_space_iter_end = 330
		self.min_empty_space_points = 75 #hesaplanacak
		self.lidar_iter_mid = 165
		self.lidar_angle_increment = math.pi / 314.16

		#Flags
		self.origin_flag = False
		self.rviz_flag = False
		self.recovery = False

		#Recovery variables
		self.recovery_counter = 0
		self.temporary_x = 0
		self.temporary_y = 0

		self.twist_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 50)
		self.main_path_pub = rospy.Publisher("/rover/main_path", Path, queue_size = 10)
		self.subpath_pub = rospy.Publisher("/rover/sub_path", Path, queue_size = 10)
		self.trail_pub = rospy.Publisher("/rover/trail", Path, queue_size = 10)

		if self.outdoor_drive:
			odom_topic = "/odometry/filtered_map"
		else:
			odom_topic = "/odometry/filtered"

		rospy.Subscriber("/gps/fix", NavSatFix, self.gps_cb)
		rospy.Subscriber("/scan", LaserScan, self.lidar_cb)
		rospy.Subscriber("/imu/data", Imu, self.imu_cb)
		rospy.Subscriber(odom_topic, Odometry, self.odom_cb)
		rospy.Subscriber("/move_base_simple/goal", PoseStamped, self.goal_cb)
		print("Initialization is complete.")

		self.reset_nodes()
		self.main()

	def imu_cb(self, data):
		[roll, pitch, self.yaw] = euler_from_quaternion([data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]) #Convert quaternion to euler angles
		self.yaw = self.fix_yaw(self.yaw)

	def lidar_cb(self, data):
		self.latest_scan = data.ranges

	def fake_lidar_data(self):
		self.nodes = [Node(index = i, cost = 1000 if i == 11 else 1) for i in range(23)]
		for node in self.nodes:
			node.print_me()

	def gps_cb(self, data):
		self.lat = data.latitude
		self.lon = data.longitude
		#Origin chosen for ll/xy transform
		if not self.origin_flag:
			self.olat = self.lat
			self.olon = self.lon
			self.origin_flag = True

	def odom_cb(self, data):
		self.x = data.pose.pose.position.x
		self.y = data.pose.pose.position.y

	def goal_cb(self, data = None):
		if data is not None:
			self.rviz_x = data.pose.position.x
			self.rviz_y = data.pose.position.y
			self.rviz_flag = True
	
	def pub_rviz_path(self, points, main = False):
		new_path = Path()
		new_path.header.frame_id = "odom"
		poses = []

		for point in points:
			new_pose = PoseStamped()
			new_pose.pose.position.x = point[0]
			new_pose.pose.position.y = point[1]
			poses.append(new_pose)

		new_path.poses = poses

		if main:
			self.main_path_pub.publish(new_path)
		else:
			self.subpath_pub.publish(new_path)

	def pub_trail(self):
		self.trail.header.frame_id = "odom"
		poses = []

		curr_pose = PoseStamped()
		curr_pose.pose.position.x = self.x
		curr_pose.pose.position.y = self.y

		self.trail.poses.append(curr_pose)
		self.trail_pub.publish(self.trail)

	def xy_input(self):
		print("Please enter cartesian coordinates.")
		print("x position: ")
		self.target_x = float(raw_input())
		print("y position: ")
		self.target_y = float(raw_input())
		print("New target: {},{}".format(self.target_x,self.target_y))

	def rviz_input(self):
		print("Please send new target from Rviz.")
		while not self.rviz_flag:
			rospy.sleep(0.05)
		self.target_x = self.rviz_x
		self.target_y = self.rviz_y
		self.rviz_flag = False
		print("New target: {},{}".format(self.target_x,self.target_y))

	def gps_input(self):
		print("Please enter coordinates.")
		print("Latitude: ")
		self.target_lat = float(raw_input())
		print("Longitude: ")
		self.target_lon = float(raw_input())
		print("New target: {},{}".format(self.target_lat,self.target_lon))
		self.gps_to_xy()

	#Transforms latitude/longitude to cartesian coordinates
	def gps_to_xy(self):
		#For outdoor
		#self.target_y, self.target_x = gc.ll2xy(self.target_lat,self.target_lon,self.olat,self.olon)
		#For Gazebo
		self.target_y, self.target_x = self.fix_gps(gc.ll2xy(self.target_lat,self.target_lon,self.olat,self.olon))
		print('Lat: %.4f, Lon:%.4f >> X: %.2f, Y: %.2f'
      			%(self.target_lat,self.target_lon,self.target_x,self.target_y))

	#For Gazebo
	def fix_gps(self, (y, x)):
		return (-1 * y, x)
		#if x * y > 0:
		#	y *= -1
		#else:
		#	x *= -1
		#return (x,y)

	#If yaw angle is not in [-pi, +pi] range, fixes it
	def fix_yaw(self, yaw):
		while not (yaw < math.pi and yaw >= -math.pi):
			if yaw >= math.pi:
				yaw -= math.pi * 2
			elif yaw < -math.pi:
				yaw += math.pi * 2
			else:
				break
		return yaw

	def control_dist(self):
		self.dist = float(math.sqrt(math.pow((self.target_x - self.x), 2) + math.pow((self.target_y - self.y), 2)))
		return self.dist > self.dist_threshold

	def reset_twist(self):
		self.twist.linear.x  = 0
		self.twist.linear.y  = 0
		self.twist.linear.z  = 0
		self.twist.angular.x = 0
		self.twist.angular.y = 0
		self.twist.angular.z = 0
		
		#self.twist_pub.publish(self.twist)

	def go_forward(self, speed, secs):
		rate = rospy.Rate(10)
		self.twist.linear.x = speed
		for i in range(int(secs * 10)):			
			if self.control_dist():
				#self.twist_pub.publish(self.twist)
				rate.sleep()
			else:
				break
		self.reset_twist()

	def turn(self, speed, secs):
		rate = rospy.Rate(10)
		self.twist.angular.z = speed
		for i in range(int(secs * 10)):
			#self.twist_pub.publish(self.twist)
			rate.sleep()
		self.reset_twist()

	def turn_to_yaw(self, target_yaw, angle_error_threshold = math.pi / 21):
		print("Current yaw: {}\nTurning to: {}".format(self.yaw, target_yaw))
		yaw_dist = self.yaw - target_yaw
		yaw_dist_complement = (math.pi * 2 - yaw_dist) * -1

		if yaw_dist > math.pi or yaw_dist < -math.pi:
			yaw_dist = yaw_dist_complement

		while (yaw_dist > angle_error_threshold) or (yaw_dist < -1 * angle_error_threshold):
			if not self.control_dist():
				break
			if (self.yaw < 0 and target_yaw > 0 and (yaw_dist > math.pi or yaw_dist < -math.pi)):
				self.turn(math.copysign(1, yaw_dist), 0.15)
			else:
				self.turn(math.copysign(1, -1 * yaw_dist), 0.15)
			self.yaw = self.fix_yaw(self.yaw)
			yaw_dist = self.yaw - target_yaw
			yaw_dist_complement = (math.pi * 2 - yaw_dist) * -1

			if yaw_dist > math.pi or yaw_dist < -math.pi:
				yaw_dist = yaw_dist_complement

	def rotate(self, target_angle = None):
		if target_angle is None:
			angle = math.atan2((self.target_y - self.y) * 1000, (self.target_x - self.x) * 1000)
		else:
			angle = target_angle

		self.turn_to_yaw(angle)

	def reset_nodes(self):
		self.nodes = [Node(index = i) for i in range(23)]

	#Spawns nodes up to 23, for outdoor
	def spawn_nodes(self, scan = None):
		self.reset_nodes()
		scan_data = list(scan)

		if scan_data[0] == float('Inf'): scan_data[0] = 5.0
		if scan_data[329] == float('Inf'): scan_data[329] = 5.0

		print("Scan data:\n{}".format(scan_data))

		iter_start = 0
		iter_end = 0
		nodes_in_row = 0
		node_counter = 0

		for i in range(self.empty_space_iter_start, self.empty_space_iter_end):
			if (scan_data[i] == float('Inf') and iter_start == 0):
				iter_start = i
			elif iter_start != 0:
				if(scan_data[i] != float('Inf') or i == self.empty_space_iter_end - 1):
					iter_end = i

			if iter_end - iter_start >= self.min_empty_space_points:
				for j in range(iter_start, iter_end + 1):
					if (j % 15) == 0:
						nodes_in_row += 1

				if nodes_in_row >= self.min_nodes:
					dist_min = min([scan_data[iter_end], scan_data[iter_start - 1]])
					dist_max = max([scan_data[iter_end], scan_data[iter_start - 1]])
					dist_per_node = (dist_max - dist_min) / (nodes_in_row - 1)

					for j in range(iter_start + 15, iter_end + 1 - 15):
						if (j % 15) == 0:
							node_index = (j / 15)
							node_yaw = self.node_angle - node_index * (self.node_angle / 11)
							yaw_dist = math.atan2((self.target_y - self.y), (self.target_x - self.x))
							cost_yaw = abs(self.fix_yaw(self.yaw + node_yaw - yaw_dist)) #WIP
							#min_dist = min([scan_data[iter_start - 1], scan_data[iter_end]])
							
							#if j >= (iter_end + iter_start) / 2:
							#	min_dist = scan_data[iter_end]
							#else:
							#	min_dist = scan_data[iter_start - 1]

							min_dist = dist_min + dist_per_node * node_counter
							
							self.nodes[node_index] = Node(iter_start = iter_start, iter_end = iter_end, index = node_index, nodes_in_row = nodes_in_row, node_yaw = node_yaw, cost_yaw = cost_yaw, min_dist = min_dist)
							node_counter += 1

				iter_start = 0
				iter_end = 0
				nodes_in_row = 0
				node_counter = 0

			elif iter_start != 0 and iter_end != 0 and (iter_end - iter_start < self.min_empty_space_points):
				iter_start = 0
				iter_end = 0
				nodes_in_row = 0
				node_counter = 0

		for node in self.nodes:
			node.print_me()
	
	#Selects the best node for navigation between spawned 23 nodes
	def best_node(self, nodes = None):
		if nodes is None:
			self.spawn_nodes(self.latest_scan)
		else:
			self.nodes = nodes

		sorted_nodes = sorted(self.nodes, key = lambda node: node.cost, reverse = True)
		
		for node in sorted_nodes:
			for i in range(-1 * node.check_nodes, node.check_nodes + 1):
				try:
					if self.nodes[node.index + i].cost == -10:
						break
					elif i == node.check_nodes:
						return node
				except:
					break

	#Navigates to the selected node
	def local_plan(self, debug = False):
		if self.debug_nodes:
			print("Waiting for response to continue...")
			_ = raw_input()

		if debug:
			best_node = self.best_node(self.nodes)
		else:
			best_node = self.best_node()

		if best_node is None:
			print("No node created.")
			self.recovery = True
			return self.recovery

		print("\nBest Node\n")
		best_node.print_me()

		if self.debug_nodes:
			print("Waiting for response to continue...")
			_ = raw_input()

		self.turn_to_yaw(self.fix_yaw(self.yaw + best_node.node_yaw))
		self.pub_rviz_path([[self.x, self.y], [self.target_x, self.target_y]])
		self.go_forward(1, self.speed)
		self.pub_trail()

	#Recovery maneuver when there are no possible nodes 
	def recovery_plan(self):
		print("Recovery started.")
		recovery_counter = 0
		self.temporary_x = self.target_x
		self.temporary_y = self.target_y

		disty = abs(self.target_y - self.y)
		distx = abs(self.target_x - self.x)

		if recovery_counter == 0:		
			if disty < distx:
				self.target_y = self.y
			else:
				self.target_x = self.x
			recovery_counter += 1
		pass #WIP!!!

	def main(self):
		if not self.lidar_used:
			self.fake_lidar_data()
		if self.outdoor_drive:
			self.speed = 2
		else:
			self.speed = 0.5
		rate = rospy.Rate(0.5)

		print("Pick a mode \n1. Outdoor \n2. Indoor \n3. Rviz") 
		selection = int(raw_input())

		while self.latest_scan is None:
			rospy.sleep(0.1)

		while not rospy.is_shutdown():
			if selection == 1:
				self.gps_input()
			elif selection == 2:
				self.xy_input()
			elif selection == 3:
				self.rviz_input()
			else:
				raise Exception('Wrong input.')

			self.trail = Path()
			self.pub_trail()

			self.pub_rviz_path([[self.x, self.y], [self.target_x, self.target_y]], main = True)

			self.rotate()
			
			while self.control_dist():
				if self.dist <= 1.0:
					self.rotate()
				print("Distance to target: {}".format(self.dist))
				self.local_plan(debug = not self.lidar_used)

				if self.recovery:
					print("Recovery started")
					self.reset_twist()
					break

			print("Target reached. Waiting for new target.")
			rate.sleep()

		rospy.spin()

if __name__ == '__main__':
	Autonomous()
