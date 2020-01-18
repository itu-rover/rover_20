#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy

class EmptySpace():
	def __init__(self, iter_av = 0, iter_start = 0, iter_finish = 0, angle_increment = 0):
		self.scan_range = rospy.get_param("lidar/obstacle_range", 3.0)
		self.iter_av = iter_av #Middle iteration point
		self.iter_start = iter_start #Start iteration point
		self.iter_finish = iter_finish #Finish iteration point
		self.angle_increment = angle_increment #Angle increment between iterations
		self.find_empty_space()

	def find_empty_space(self):
		self.angle = abs(self.iter_finish - self.iter_start) * self.angle_increment * math.pi #Angle between lines
		self.first_dist = self.scan_range / math.cos(abs(self.iter_start - self.iter_av) * self.angle_increment) #Length of first line
		self.second_dist = self.scan_range / math.cos(abs(self.iter_finish - self.iter_av) * self.angle_increment) #Length of second line
		self.space_width = math.sqrt(self.first_dist ** 2 + self.second_dist ** 2 - 2 * self.first_dist * self.second_dist * math.cos(self.angle)) #Width of empty space using cos theorem

	def print_me(self):
		print("Iter start: {}\nItem finish: {}\nAngle increment: {}\nEmpty space width: {}\nFirst line length: {}\nSecond line length: {}\nAngle: {}\n\n".format(
			self.iter_start, self.iter_finish, self.angle_increment, self.space_width, self.first_dist, self.second_dist, self.angle))