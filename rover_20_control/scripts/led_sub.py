#!/usr/bin/env python
# 2018 ERC subs all joys ,  pubs to serial led node
# ITU Rover Team
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from  rover_control.msg import *

sent_disable_msg=True


orange=1
red=2
green=3

pub=rospy.Publisher("/rover_serial/led", String, queue_size=10)

def callbackarm(data):
	global  sent_disable_msg
	sent_disable_msg = False
	pub.publish(str(green))
	
		
def callbackdrill(data):
	global  sent_disable_msg
	sent_disable_msg = False
	pub.publish(str(green))
	
		
def callbackshovel(data):
	global  sent_disable_msg
	sent_disable_msg = False
	pub.publish(str(green))
	

def callbackjoy(data):
   
	global  sent_disable_msg
	if(data.linear.x != 0 or  data.angular.z != 0):
		sent_disable_msg = False
		pub.publish(str(green))


def callbacknavcmd(data):
   
	global  sent_disable_msg
	if(data.linear.x != 0 or  data.angular.z != 0):
		sent_disable_msg = False
		pub.publish(str(red))

def main():
	
	rospy.init_node('rover_led')

	rate = rospy.Rate(0.5)
	rospy.Subscriber("/arm_teleop", Arm_msgs, callbackarm)
	rospy.Subscriber("/drill_teleop", Arm_msgs, callbackdrill)
	rospy.Subscriber("/shovel_teleop", Arm_msgs, callbackshovel)
	rospy.Subscriber("/rover_joy/cmd_vel",Twist, callbackjoy)
	rospy.Subscriber("/rover_navigation/cmd_vel",Twist, callbacknavcmd)
    
	global sent_disable_msg
	
	while  not rospy.is_shutdown():
	  if(sent_disable_msg == False):

		 sent_disable_msg=True	
		 
	  else:
		 sent_disable_msg=True
		 pub.publish(str(orange))
		 
	
	  rate.sleep()
	 
	rospy.spin()

if __name__ == '__main__':
		main()
		rospy.spin()