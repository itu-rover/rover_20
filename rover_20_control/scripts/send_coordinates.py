#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 2018 ERC sends 2d coordinates into  ref frame
# ITU Rover Team
import rospy
from std_msgs.msg import String
from move_base_msgs.msg import MoveBaseAction,MoveBaseGoal
import actionlib
import tf
client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
string_iki_nokta= ' '
def move():
	
	global client,  string_iki_nokta
	print(" client is waiting")
	client.wait_for_server()
	print(" client is on")
	string_status=' '

	while not rospy.is_shutdown():
		if(string_status =='e '):
			break
		elif (string_status !='e'):
			string_status=' '
			print("iki nokta verelim mi    evet icin k hayir icin l")
			string_iki_nokta = raw_input()
			if(string_iki_nokta=='k'):
				print("Enter x1  ")
				string_x1 = raw_input()
				print("Enter y1  ")
				string_y1 = raw_input()
				print("Enter yaw angle1 ")
				string_yaw1 = raw_input()
				 
			print("Enter x  ")
			string_x = raw_input()
			print("Enter y  ")
			string_y = raw_input()
		
			if(string_iki_nokta=='k'):
				send_move_base(float(string_x1) , float(string_y1))
			send_move_base(float(string_x), float(string_y))

			while(string_status != 'c'):
				print("Pause goal for p , Resume goal for r , abort goal for q , new goal for c , exit for e ")
				string_status= raw_input()
				if(string_status =='p'):
					print("Pausing")
					pause_move_base()
				elif(string_status=='r'):
					print("Resuming")
					send_move_base(float(string_x), float(string_y),float(string_yaw))
				elif(string_status=='q'):
					print("Aborting")
					pause_move_base()
				elif(string_status=='e'):
					print("Exiting from program..")
					break
				elif(string_status=='c'):
					break


def  send_move_base(x, y):
	
	global client, string_iki_nokta
	goal=MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"

	goal.target_pose.pose.position =  Point(x,y,0)
	goal.target_pose.pose.orientation.x = 0.0
	goal.target_pose.pose.orientation.y = 0.0
	goal.target_pose.pose.orientation.z = 0.0
	goal.target_pose.pose.orientation.w = 1.0 
  
	client.send_goal(goal)
	if(string_iki_nokta=='k'):
		wait = client.wait_for_result()
		string_iki_nokta=' '
	#wait = client.wait_for_result()
def  pause_move_base():
	global client
	goal=MoveBaseGoal()
	goal.target_pose.header.frame_id = "map"
	client.cancel_all_goals()
	client.cancel_goal()




if __name__ == '__main__':
	try:
		rospy.init_node('send_coordinates')
		move()
	except rospy.ROSInterruptException:
		rospy.loginfo("Exception thrown")

