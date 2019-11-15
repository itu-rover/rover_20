#!/usr/bin/env python
import sys
import rospy
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import Joy
from tf.transformations import *
from tf.msg import tfMessage
from math import pi
import moveit_commander
import moveit_msgs.msg

rospy.init_node('linear_actuator',anonymous=True)
moveit_commander.roscpp_initialize(sys.argv)

group_name = "eski"
global group
group = moveit_commander.MoveGroupCommander(group_name)
joint_goal = group.get_current_joint_values()

def callback(data):

    while not rospy.is_shutdown():

        if data.buttons[4] == 1 and data.buttons[5] == 1 and data.axes[1] != 0:
            print "data"

            joint_goal = group.get_current_joint_values()
            joint_goal[0] = joint_goal[0]         #joint1
            joint_goal[1] = joint_goal[1]        #joint2
            joint_goal[2] = joint_goal[2]         #joint3
            joint_goal[3] = joint_goal[3]+data.axes[1]*pi/36         #joint4
            joint_goal[4] = joint_goal[4]        #joint5
            joint_goal[5] = joint_goal[5]         #joint6
            print joint_goal
            group.go(joint_goal, wait=True)
        elif data.buttons[4] == 0 and data.buttons[5] == 1 and data.axes[1] != 0:
            print "data"
            joint_goal = group.get_current_joint_values()
            joint_goal[0] = joint_goal[0]        #joint1
            joint_goal[1] = joint_goal[1]+data.axes[1]*pi/36           #joint2
            joint_goal[2] = joint_goal[2]      #joint3
            joint_goal[3] = joint_goal[3]      #joint4
            joint_goal[4] = joint_goal[4]        #joint5
            joint_goal[5] = joint_goal[5]        #joint6
            print joint_goal
            group.go(joint_goal, wait=True)
        elif data.buttons[4] == 0 and data.buttons[5] == 1 and data.axes[1] != 0:
            print "data"
            joint_goal = group.get_current_joint_values()
            joint_goal[0] = joint_goal[0]         #joint1
            joint_goal[1] = joint_goal[1]          #joint2
            joint_goal[2] = joint_goal[2]          #joint3
            joint_goal[3] = joint_goal[3]         #joint4
            joint_goal[4] = joint_goal[4]+data.axes[0]*pi/36          #joint5
            joint_goal[5] = joint_goal[5]        #joint6
            print joint_goal
            group.go(joint_goal, wait=True)
def main():
    rospy.Subscriber("joy", Joy, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
