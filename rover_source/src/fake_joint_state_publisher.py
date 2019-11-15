#!/usr/bin/env python
# -*- coding: utf-8 -*-



import rospy
from sensor_msgs.msg import JointState


class joint_states(object):
	def __init__(self):



		rospy.init_node("fake_joint_state_publisher")
		self.pub = rospy.Publisher("/joint_states", JointState, queue_size = 50)

		self.data = JointState()

		self.rate = rospy.Rate(30)

		self.data.name = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]
		self.data.position = [1, 1, 1, 1, 1, 1]
		self.data.effort = [10,10,10,10,10,10]

		while not rospy.is_shutdown():
			
		
			self.state_publisher()
			print(self.data)

			self.rate.sleep()

			

	def state_publisher(self) :

		self.pub.publish(self.data)

if __name__ == '__main__':
	joint_states()
