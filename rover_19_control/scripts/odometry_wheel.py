#!/usr/bin/env python

import rospy
from std_msgs.msg import String


if __name__ == '__main__':

	rospy.init_node('odometry_wheel_publisher')

	pub = rospy.Publisher("/message", String, queue_size=10)

	rate = rospy.Rate(10)

	while not rospy.is_shutdown():

		pub.publish('msg gfghj')

		rate.sleep()


