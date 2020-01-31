from math import *

class Arm(object):
	def __init__(self):
		self.lengths = [14.0,50.0,42.0,11.0,10.0]

		#self.limits =
		self.ub=[pi,pi/2,0.9,pi/3,pi/2]
		self.lb=[-pi,-pi/3,-0.9,-pi,-pi/2]
		# Joint names for specifying which joint has reached its limits
		self.joint_angles = [0.0, pi/2, pi/2, 0.0, 0.0,0.0]
		self.initial_angles = [0.0, pi/2, pi/2, 0.0, 0.0,0.0]
