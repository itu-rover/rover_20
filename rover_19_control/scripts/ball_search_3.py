#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped,Twist
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from rover_state_mach.msg import RoverStateMsg
import tf

class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('ball_search', anonymous=False)
        self.currPosX=0
        self.currPosY=0
        self.currPosZ=0
        self.yaw=0
        self.rotate_once=1
        self.send_once=1
        self.R=0.5
        self.ball_is_found=0
        self.state=RoverStateMsg()
        print("waiting move base client...")
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        print("client is on")
        rate = rospy.Rate(10) # 1hz
        #tell the action client that we want to spin a thread by default
        self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        

        while not rospy.is_shutdown():
            rospy.Subscriber('/outdoor_waypoint_nav/odometry/filtered',Odometry, self.robotPoseSubscriber)
            rospy.Subscriber('/rover_state_topic',RoverStateMsg, self.stateSubscriber)
            #rospy.Subscriber('/move_base/result',MoveBaseActionResult, self.moveSubscriber)
            #print(self.state.state)
            if(self.state.state==self.state.FIND_IMAGE):
                if( self.rotate_once==1):
                    print("searching")
                    self.go_forward()
                    self.rotate(180)
                    self.rotate(-180)
                    self.rotate_once=0

                if(self.state.state==self.state.FIND_IMAGE):
                    self.go_forward()
                if(self.state.state==self.state.FIND_IMAGE):
                    self.rotate(90)
            else:
                print("waiting")

        
            rate.sleep()

    def stateSubscriber(self,stateMsg):
        self.state=stateMsg
        if(self.state.state==self.state.REACH_IMAGE):
            if(self.send_once==1):
                print("found image")
                self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) 
                self.twist = Twist()
                self.twist.linear.x=0
                self.twist.angular.z=0
                self.Pub.publish(self.twist)
                self.client.cancel_goal()
                self.client.cancel_all_goals()
                self.send_once=0



    def robotPoseSubscriber(self,poseMsg): #Odometry update recieved from ROS topic, run this function
    
        self.currPosX = poseMsg.pose.pose.position.x
        self.currPosY = poseMsg.pose.pose.position.y
        self.currPosZ = poseMsg.pose.pose.position.z
        self.currOrX = poseMsg.pose.pose.orientation.x
        self.currOrY = poseMsg.pose.pose.orientation.y
        self.currOrZ = poseMsg.pose.pose.orientation.z
        self.currOrW = poseMsg.pose.pose.orientation.w

        quaternion = (
        poseMsg.pose.pose.orientation.x,
        poseMsg.pose.pose.orientation.y,
        poseMsg.pose.pose.orientation.z,
        poseMsg.pose.pose.orientation.w)
        euler = tf.transformations.euler_from_quaternion(quaternion)
        self.roll = euler[0]
        self.pitch = euler[1]
        self.yaw = euler[2]

    def go_forward(self):

        print("Going forward...")
        goal=MoveBaseGoal()
        goal.target_pose.header.frame_id = "/base_link"
        dist=1                                                  #1 metre ileri gidiyor 
        goal.target_pose.pose.position.x = dist
        goal.target_pose.pose.position.y =0
        goal.target_pose.pose.position.z = 0

        q = tf.transformations.quaternion_from_euler(0,0,0)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3] 

        self.client.send_goal(goal)
        wait = self.client.wait_for_result()
        dist=dist+0.5

    def rotate(self, angle):     
        print("Rotating...")
        #print(angle)
        goal = MoveBaseGoal()
         
        goal.target_pose.header.frame_id = "/base_link"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x =0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0 

        q = tf.transformations.quaternion_from_euler(0,0,(float(angle)*pi/180))
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y =q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3] 
         
        self.client.send_goal(goal)
        wait = self.client.wait_for_result()
    def rotate_2(self):
        self.twist = Twist()
        self.twist.angular.z=0.5
        self.twist.linear.x=0
        self.Pub.publish(self.twist)
   
    
if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")