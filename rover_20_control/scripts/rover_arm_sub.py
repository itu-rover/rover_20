#!/usr/bin/env python
# 2018 ERC subs joy arm ,  pubs to serial node
# " S + joint_1 + joint_2+ joint_3 + joint_4 + joint_5 +joint_6 + F"
# J4 and J5 has incremental stabile variables which is  angle position , others only PWM
# ITU Rover Team
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from  rover_control.msg import *

old_joint3 = 0
old_joint4 = 0
joint3=0
joint4=0
arm =Arm_msgs()

pub=rospy.Publisher("/rover_serial/arm_01256", String, queue_size=50)
pub1=rospy.Publisher("/rover_serial/arm_34", String, queue_size=50)

def callbackarm(data):
    arm=data
    global old_joint3
    global old_joint4
    global joint3
    global joint4
    
    joint0_str=floattostring(arm.joint0,300)
    joint1_str=floattostring(arm.joint1,700)
    joint2_str=floattostring(arm.joint2,700)
    joint5_str=floattostring(arm.joint5,200)
    joint6_str=floattostring(arm.joint6,999)
 
    
    joint3=incrementalfloat(arm.joint3,10,old_joint3)
    joint3_str=floattostring(joint3,1)
    old_joint3=joint3

    joint4=incrementalfloat(arm.joint4,10,old_joint4)
    joint4_str=floattostring(joint4,1)
    old_joint4=joint4

    pub.publish("S"+joint0_str+joint1_str+joint2_str+joint5_str+joint6_str+"F")
    pub1.publish("S"+joint3_str+joint4_str+"F")
def main():
  
    rospy.init_node('rover_arm_sub_serial')
    rospy.Subscriber("/arm_teleop", Arm_msgs, callbackarm)

    #pub1.publish("S"+joint3_str+joint4_str+"F")
    rospy.spin()

def floattostring(joint, scalar):
    if joint<0 :
        value = int(joint*-scalar)
        if value<10:
            string = "000"+str(value)
        elif value< 100 and value > 9:
           string = "00"+str(value)
        else:
            string= "0"+str(value)
    else:
        value= int(joint*scalar)
        if value<10:
            string= "100"+str(value)
        elif value < 100 and value > 9:
            string = "10"+str(value)
        else:
            string = "1"+str(value)
    return string
def incrementalfloat(joint, scalar,old_value):
    value=0
    if joint<0 :
        value =  old_value-scalar
        if value<-180:
           value=-180

    elif joint>0:
        value = old_value+scalar
        if value >180:
            value=180 
    else :
        value=old_value
    return value

if __name__ == '__main__':
    main()
    rospy.spin()