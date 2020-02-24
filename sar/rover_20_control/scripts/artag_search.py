#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal, MoveBaseActionResult
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import PoseStamped,Twist
from math import radians, cos, sin, asin, sqrt, pow, pi, atan2
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from rover20_state_mach.msg import StateMsg
from sensor_msgs.msg import Imu
#from rover_servo_serial import Servocamera
import tf
import time

#Servocamera = Servocamera()
# Changes are made by Berke Algul and in 24.12.2019
# Changes are made by Berke Algul and Murruvet Bozkurt in 7.2.2020

class GoForwardAvoid():
    def __init__(self):
        rospy.init_node('ball_search', anonymous=False)
        self.currPosX=0
        self.currPosY=0
        self.currPosZ=0
        self.yaw=0
        self.startMsg = "s10f"
        self.stopMsg = "s01f"
        self.rotate_once=1 # deleted in code
         # if servo completed its rotation this will be true
        self.send_once=1
        self.R=0.5
        self.ball_is_found=0
        self.dir = 1
        self.sangle = 0 #servo angle
        self.sc = None
        self.left = None  #left artag
        self.right = None #right artag
        self.rotate_done = None
        self.half_rotate = False
        self.state=StateMsg()
        #self.donedone = Servocamera.done_servo_rotation()
        print("waiting move base client...")
        self.client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
        self.client.wait_for_server()
        print("client is on")
        rate = rospy.Rate(10) # 1hz
        #tell the action client that we want to spin a thread by default
        self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.Servo_pub = rospy.Publisher('/servo_control', String, queue_size=10)

        self.rover_rotated = False
        self.servo_rotating = False
        self.servo_rotated = False
        self.servo_rotation_count = 0

        while not rospy.is_shutdown():
            rospy.Subscriber('/outdoor_waypoint_nav/odometry/filtered',Odometry, self.robotPoseSubscriber)
            rospy.Subscriber('/rover_state_topic',StateMsg, self.stateSubscriber)
            rospy.Subscriber('/stage_counter_topic', String, self.stageSubscriber)
            rospy.Subscriber('/servo_angle', String, self.angleSubscriber)
            #rospy.Subscriber('/imu/data', Imu, self.imuSubscriber)
            #print(self.state.state)
            #print("rotate_done:",  self.rotate_done)
            
            #rospy.Subscriber('/move_base/result', MoveBaseActionResult, self.moveSubscriber) ##
            #print(self.state.state)
            if (self.state.state==self.state.FIND_ARTAG):
                rospy.Subscriber('/px_coordinates', String, self.artag_Subscriber)
                rospy.Subscriber('/px_coordinates1', String, self.artag_Subscriber1)
                rospy.Subscriber('/servodone', String, self.done_rotate_Subscriber)

                print("searching")
                #print("servo_rotated: ", self.servo_rotated)
                print("servo rotating: ", self.servo_rotating)
                print("servo_rotation_count: ", self.servo_rotation_count)


                if self.servo_rotating == False:
                    if self.servo_rotation_count == 0:
                        self.start_servo_rotation()
                        self.servo_rotating = True
                        print("mgbncmb")
                        continue

                    if self.rover_rotated == False and self.servo_rotation_count == 1:            
                        self.rotate(90)
                        time.sleep(15)
                        self.servo_rotated = False
                        self.rover_rotated = True
                        print("rover rotated")
                        if(self.servo_rotated == False and self.rover_rotated == True):
                            self.start_servo_rotation()
                            time.sleep(5)
                            continue
                        
                    if(self.rover_rotated == True and self.servo_rotation_count == 2):
                        print("ZIGZAG veya SALYANGOZ")
                        #print("jnbxfjbnfxjbmnbjnbjxnbjxfnbkxjnb jfnbjkfnbkjnbkjcvnbjcnbkjbnkcnbkcngbkdghbkjdnbfhnmvnbjkghjfcnbfjkfhgbfjvb gjdgbhdjkdvbngdjmvnbgdjmvdb mvfsmycebntjtghekjgtnbwtkxfwnbwdjkwhnbw jtmxvcn btwjcmtnbw tjcwvnb tjwdnhtjkbw nvcwtwtwttery")

                        self.go_forward()
                        self.rotate(90)
                        
                        if(self.sc >= 4 and self.left == True and self.right == False):
                            self.go_forward()
                            self.rotate(-90)
                            self.go_forward()   
                            self.rotate(90)


                        if(self.sc >= 4 and self.right == True and self.left == False):
                            self.go_forward()
                            self.rotate(90)
                            self.go_forward()
                            self.rotate(-90)

                        self.rover_rotated = False
                        self.servo_rotation_count = 3
                        self.servo_rotated = False
            elif(self.state.state==self.state.REACH_ARTAG or self.state.state == self.state.APPROACH):
                print("REACH_ARTAG!!!!!!!")
                        
            else:
                print("waiting")

            rate.sleep()


    def stateSubscriber(self,stateMsg):
        self.state=stateMsg
        if(self.state.state==self.state.REACH_ARTAG or self.state.state == self.state.APPROACH):
            if(self.send_once==1):
                print("found artag")
                self.stop_servo_rotation() #stop servo
                time.sleep(3)
                rospy.Subscriber('/servo_angle', String, self.angleSubscriber) #subscribe servo angle
                #self.Pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
                #time.sleep(5) 
                self.sangle =0-int(self.sangle[:2])
                print("ANGLE OF SERVO CAMERA: ", self.sangle)
                time.sleep(2)
                #rospy.Subscriber('/imu/data', Imu, self.imuSubscriber)
                #self.previousYaw = self.currImuYaw
                #while(1):
                    #rospy.Subscriber('/imu/data', Imu, self.imuSubscriber)
                self.rotate(self.sangle) #Rover turns as much as the angle the servo sees the artag.
                    #if self.currImuYaw == (float(self.previousYaw) + 180) or self.currImuYaw == (float(self.previousYaw) - 180):
                        #break'''
                time.sleep(5)
                self.twist = Twist()
                self.twist.linear.x=0
                self.twist.angular.z=0
                self.Pub.publish(self.twist)
                #self.client.cancel_goal()
                #self.client.cancel_all_goals()
                self.send_once=0
                self.half_rotate = True
                if(self.half_rotate == True):
                    self.Servo_pub.publish(self.stopMsg)

    def angleSubscriber(self, data): 
        self.sangle = data.data #convert string to integer.
        #print(self.sangle)

    def stageSubscriber(self, data): #px_coordinates
        self.sc = int(data.data)
        #print("stage:", self.sc)

    def artag_Subscriber(self, data): #px_coordinates1
        self.a_coor = data.data

        if self.a_coor != "-":
            self.left = True
        else:
            self.left = False

    def artag_Subscriber1(self, data):
        self.a_coor1 = data.data

        if self.a_coor1 != "-":
            self.right = True
        else:
            self.right = False

    def done_rotate_Subscriber(self, data):
        self.rotate_done = data.data
        #print("lkdsfjfkh")
        if(self.rotate_done == "1" and self.servo_rotating == True):
            print("rotate_done is true")
            self.servo_rotating = False
            self.servo_rotation_count += 1
        '''else:
            self.servo_rotated = False'''

    '''def imuSubscriber(self,data):
        self.currImuYaw = data.orientation.z'''
    

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

        self.client.send_goal(goal) ##
        wait = self.client.wait_for_result() ##
        dist=dist+0.5

    def rotate(self, angle):     
        print("Rotating...")
        #print(angle)
        goal = MoveBaseGoal()
         
        goal.target_pose.header.frame_id = "/base_link"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = 0
        goal.target_pose.pose.position.y = 0
        goal.target_pose.pose.position.z = 0 

        q = tf.transformations.quaternion_from_euler(0,0, (float(angle)*pi/180),0)#(float(angle)*pi/180))
        goal.target_pose.pose.orientation.x = q[0]
        goal.target_pose.pose.orientation.y =q[1]
        goal.target_pose.pose.orientation.z = q[2]
        goal.target_pose.pose.orientation.w = q[3] 
         
        self.client.send_goal(goal)
        wait = self.client.wait_for_result()

    """def rotate(self, angle):
        print("Rotating...")
        self.twist = Twist()
        self.twist.angular.z=8
        self.twist.linear.x=0
        self.Pub.publish(self.twist)"""

    #def rotate_cam(self):
        # this is the function that makes arduino rotate servo
        #self.Servo_pub.publish("s" + 10 + "f")
        #pass

    def start_servo_rotation(self):
        self.Servo_pub.publish(self.startMsg)
        #self.servo_rotated = False
        self.servo_rotating = True
        #self.servo_rotation_count += 1
        print("servo has started to rotate.")

    def stop_servo_rotation(self):
        self.Servo_pub.publish(self.stopMsg)
        #self.servo_rotated = True
        self.servo_rotating = False
        print("servo had stopped")
        self.servo_rotation_count = 4 
    
    '''def look_around(self): #TODO: add delay or logic control 

        if self.servo_rotated == False:
            self.start_servo_rotation()
               
        #elif self.servo_rotated == True:
            #self.rotate(180)
            #print("rotate is finished!")
            #self.servo_rotated = False
            #self.start_servo_rotation()

        rover_rotated = False

        while not rospy.is_shutdown():
            #servo sub
            if self.servo_rotated is True:
                self.rotate(180)
                time.sleep(5)
                rover_rotated = True
                print("rover's rotation is finished!")
                #self.servo_rotated =False
                #stop_servo_rotation()

            if rover_rotated  is True and self.servo_rotated is True:
                self.servo_rotated = False
                break'''
            

if __name__ == '__main__':
    try:
        GoForwardAvoid()
    except rospy.ROSInterruptException:
        rospy.loginfo("Exception thrown")
