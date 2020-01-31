#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal,MoveBaseActionResult
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped, Twist
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import tf
from rover20_state_mach.msg import RoverStateMsg


class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('ball_handler', anonymous=False)
        self.currPosX=0
        self.currPosY=0
        self.currPosZ=0
        self.yaw=0
        self.bearingToball=0.0
        self.bearingToball_old=0.0
        self.counter=0
        self.send_once=1
        self.ball_is_found=0
       
        self.msg="-"
        self.state=RoverStateMsg()
        self.move_msg=MoveBaseActionResult()
        self.twist = Twist()
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        print("waiting client server")
        self.client.wait_for_server()
        print(" client is on")
        rate = rospy.Rate(10) # 10hz
        #tell the action client that we want to spin a thread by default
        self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #Publish Nav Goal to ROS topic
        self.Pub2=rospy.Publisher('/image_reach_topic',String,queue_size=10)  #Publisher oluşturduk
        self.count = 0
        while not rospy.is_shutdown():

            rospy.Subscriber('/outdoor_waypoint_nav/odometry/filtered',Odometry, self.robotPoseSubscriber)
            rospy.Subscriber('/rover_state_topic',RoverStateMsg, self.stateSubscriber)
            rospy.Subscriber('/bearing_to_ball',String, self.ballYawSubscriber)
            rospy.Subscriber('/move_base/result',MoveBaseActionResult, self.moveSubscriber)
            print(str(self.state.state))
            
            #self.msg=self.ballYawSubscriber
            '''self.state.state=self.state.REACH_IMAGE '''   #changed
            if(self.state.state==self.state.REACH_IMAGE):
                #print(self.state.state)     #eklendi
                if(self.msg=="-"):       #(self.msg=="-")
                   print("ball is not found")
                   twist_empty=Twist()
                   self.Pub.publish(twist_empty)
                   self.Pub2.publish("0")    #eklendi


                else:
                    print(self.msg)   #self.msg
                    bear = abs(float(self.msg))
                    self.bearingToball= float(self.msg)*pi /180
                    self.Pub2.publish("0")     #eklendi
                    if bear> 5:
                        self.rotate_to_ball_2()

                    elif bear <= 5:
                        self.twist.angular.z=0
                        self.Pub.publish(self.twist)
                        self.Pub2.publish("0")      #eklendi
                        if(self.count<3):#3
                            self.go_forward()
                        else:
                            while not rospy.is_shutdown():
                                print("Succesful")
                                self.Pub2.publish("1")     #degistirildi

        

            #rospy.spin()    
    def stateSubscriber(self,stateMsg):
        self.state=stateMsg
       
    def moveSubscriber(self,moveMsg):
        self.move_msg=moveMsg
        # print(self.move_msg.status.text)
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

    def ballYawSubscriber(self,yawMsg):
        self.msg=yawMsg.data 
        #print(self.msg)          

    def rotate_to_ball(self):
        goal=MoveBaseGoal()
        goal.target_pose.header.frame_id = "/base_link"
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0
        q = tf.transformations.quaternion_from_euler(0,0,self.bearingToball)
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y = q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3] 

        self.client.send_goal(goal)
        wait = self.client.wait_for_result()
        self.go_forward()
    
    def rotate_to_ball_2(self):
        if(self.bearingToball>0):
            self.twist.angular.z=0.4
        if(self.bearingToball<0):
            self.twist.angular.z=-0.4
                      

        self.Pub.publish(self.twist)
  
       

    def go_forward(self):

        goal=MoveBaseGoal()
        goal.target_pose.header.frame_id = "/base_link"
        dist=2
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
        self.count += 1
    

if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
