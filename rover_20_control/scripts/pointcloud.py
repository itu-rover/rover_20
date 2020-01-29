#!/usr/bin/env python
# 2018 ERC subs all joys ,  pubs to serial led node
# ITU Rover Team
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from  rover_control.msg import *
from sensor_msgs.msg import LaserScan

sent_disable_msg=True

scan = LaserScan()

pub=rospy.Publisher("/tennis_ball_with_lidar", String, queue_size=10)


def callback(data):
   
	scan.ranges = data.ranges
	scan.angle_increment = data.angle_increment
	scan.angle_min = data.angle_min
	scan.angle_max = data.angle_max

	ranges = data.ranges
	msg = "not found"
	found = 0
	for i in range(int((data.angle_max-data.angle_min)/(data.angle_increment*2))-50,int((data.angle_max-data.angle_min)/(data.angle_increment*2))+50):
		if(ranges[i]<1.0):
			print("ball is found")
			found = 1
	
	if(found == 0):
		print("not found")
	

def main():
	
	rospy.init_node('scan_subscriber')

	rate = rospy.Rate(5)
	rospy.Subscriber("/scan",LaserScan, callback)
    
	rospy.spin()
	#while  not rospy.is_shutdown():
	#print(scan.ranges)

	 

if __name__ == '__main__':
		main()