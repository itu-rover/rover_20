#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import rospy

class Node():
	def __init__(self, iter_start = 0, iter_end = 0, index = 0, nodes_in_row = 0, node_yaw = 0, cost_yaw = 0, min_dist = 0, node_scan = None):
		self.iter_start = iter_start
		self.iter_end = iter_end
		self.iter_mid = (self.iter_start + self.iter_end) / 2
		self.index = index
		self.nodes_in_row = nodes_in_row
		self.node_yaw = node_yaw
		self.min_dist = min_dist #min distance to obstacle
		self.cost_yaw = cost_yaw
		self.min_dist_param = 0
		self.node_scan = node_scan

		if self.min_dist != 0:
			self.find_interval()
		else:
			self.check_nodes = 0

		if self.iter_start != 0 or self.iter_end != 0:
			self.cost_function()
		else:
			self.cost = -10

	def find_interval(self):
		if self.min_dist >= 1 and self.min_dist < 1.2:
			self.check_nodes = 5
		elif self.min_dist >= 1.2 and self.min_dist < 1.5:
			self.check_nodes = 4
		elif self.min_dist >= 1.5 and self.min_dist < 2:
			self.check_nodes = 3
		elif self.min_dist >= 2 and self.min_dist < 3.4:
			self.check_nodes = 2
		elif self.min_dist >= 3.4:
			self.check_nodes = 1
		elif self.min_dist < 1:
			self.check_nodes = 6
	
	def cost_function(self):
		#self.cost = math.sqrt((self.nodes_in_row)) + 2.345 * (1 / (self.cost_yaw + 0.0000001))
		self.cost = (self.cost_yaw + 0.0000001) + math.pow((1 / self.nodes_in_row), 2) + (1 / self.min_dist) * 6
	
	def print_me(self):
		print("Index: {}\nIter start: {}\nIter end: {}\nMin dist: {}\nNode yaw: {}\nCost yaw: {}\nNodes in row: {}\nCost: {}\nCheck Nodes: {}\nNode scan: {}\n".format(
			self.index, self.iter_start, self.iter_end, self.min_dist, self.node_yaw, self.cost_yaw, self.nodes_in_row, self.cost, self.check_nodes, self.node_scan))