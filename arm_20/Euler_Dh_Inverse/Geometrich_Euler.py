#!/usr/bin/env python2
import rospy
import math
from std_msgs.msg import Float64 as F64
from random import randint
from sensor_msgs.msg import Joy

global px,pxi,py,pyi,pz,pzi,w,flag,button,L_1,L_2,L_3,L_4,L_5,L_6,t0,t1,t2,t3,t4,t5
t0=0
t1=0
t2=0
t3=0
t4=0
t5=0
math.pi/2
px=0.03
py=0.2
pz=-0.38
pxi=0
pyi=0
pzi=0
button=0
pitch=1.66
yaw=0.12
roll=0.232
pitchi=0
yawi=0
rolli=0

L_1 = 14
L_2 = 50
L_3 = 42
L_4 = 11
L_5 = 0
L_6 = 10

def callback(data):

    global pxi,pyi,pzi,button,pitch,yaw,roll,L_1,L_2,L_3,L_4,L_5,L_6,t0,t1,t2,t3,t4,t5,rolli,pitchi,yawi
    button=data.buttons[4]
    pxi=data.axes[0]*0.05
    pyi=data.axes[1]*0.05
    pzi=data.axes[5]*0.05
    pitchi=data.axes[3]*0.05
    yawi=data.axes[2]*0.05
    rolli=data.axes[4]*0.05

def Euler_Inverse(Px,Py,Pz,x,y,z):
    global pz,py,px,t0,ti0,t1,ti1,t2,ti2,t3,ti3,t4,ti4,t5,ti5
    L1_2=0.44
    L2_3=0.31
    r=math.sqrt(pow(px,2)+pow(py,2)+pow(pz,2))
    alpha=math.asin(pz/r)
    Omega=math.atan2(L2_3*math.sin(t2),L1_2+L2_3*math.cos(t2))
    o=(pow(px,2)+pow(py,2)+pow(pz,2)-pow(L1_2,2)*pow(L2_3,2))/(2*L1_2*L2_3)

    

    t0=math.atan2(py,px)
    t2=-math.acos(o)

    t1=alpha+Omega

    #t1=math.atan2(math.sqrt(1-pow(o,2)),-o)
    #t2=math.asin(z/r)+math.atan2(L1_2*math.sin(t2),L0_1+(L1_2*math.cos(t2)))
    
    u=-math.cos(t0)*(math.cos(z)*math.sin(x)-math.cos(x)*math.sin(y)*math.sin(z))-math.sin(t0)*(math.sin(x)*math.sin(z)+math.cos(x)*math.cos(z)*math.sin(y))

    v=math.cos(x)*math.cos(y)*math.sin(t1+t2)+math.cos(t0)*math.cos(t1+t2)*(math.sin(x)*math.sin(z)+math.cos(x)*math.cos(z)*math.sin(y))-math.sin(t0)*math.cos(t1+t2)*(math.cos(z)*math.sin(x)-math.cos(x)*math.sin(y))

    t3=math.atan2(u,v)

    k=-math.sin(y)*math.cos(t1+t2)-math.cos(t0)*math.cos(y)*math.cos(z)*math.sin(t1+t2)-math.cos(y)*math.sin(t0)*math.sin(z)*math.sin(t1+t2)

    m=math.cos(y)*math.sin(x)*math.cos(t1+t2)+math.cos(t0)*math.sin(t1+t2)*(math.cos(x)*math.sin(z)-math.cos(z)*math.sin(x)*math.sin(y))-math.sin(t0)*math.sin(t1+t2)*(math.cos(x)*math.cos(z)+math.sin(x)*math.sin(y)*math.sin(z))

    

    e=math.cos(x)*math.cos(y)*math.cos(t1+t2)-math.cos(t0)*math.sin(t1+t2)*(math.sin(x)*math.sin(z)+math.cos(x)*math.cos(z)*math.sin(y))+math.sin(t0)*math.sin(t1+t2)*(math.cos(z)*math.sin(x)-math.cos(x)*math.sin(y)*math.sin(z))

    
    t4=math.atan2(e,math.sqrt((1-pow(e,2))))

    t5=math.atan2(k,m)

    #f=math.cos(t0)*(math.cos(x)*math.cos(z)+math.sin(x)*math.sin(y)*math.sin(z))+math.sin(t0)*(math.cos(x)*math.sin(z)-math.cos(z)*math.sin(x)*math.sin(y))

    #t5=math.asin((-f))-t3

    #t5=math.atan2(-f,math.sqrt((1-pow(f,2))))

    return t0,t1,t2,t3,t4,t5


if __name__ == '__main__':
    rospy.init_node('control_Deneme', anonymous=True)
    
    pub1 = rospy.Publisher('/rover_arm_j1_joint_position_controller/command', F64, queue_size=1)
    pub2 = rospy.Publisher('/rover_arm_j2_joint_position_controller/command', F64, queue_size=1)
    pub3 = rospy.Publisher('/rover_arm_j3_joint_position_controller/command', F64, queue_size=1)
    pub4 = rospy.Publisher('/rover_arm_j4_joint_position_controller/command', F64, queue_size=1)
    pub5 = rospy.Publisher('/rover_arm_j5_joint_position_controller/command', F64, queue_size=1)
    pub6 = rospy.Publisher('/rover_arm_j6_joint_position_controller/command', F64, queue_size=1)
    rospy.Subscriber("joy",Joy,callback)
    rate=rospy.Rate(150)

while not rospy.is_shutdown():
        px=px+pxi
        py=py+pyi
        pz=pz+pzi
        roll=roll+rolli
        pitch=pitch+pitchi
        yaw=yaw+yawi


        Euler_Inverse(px,py,pz,roll,pitch,yaw)

        arm_pub=[t0,t1,t2,t3,t4,t5]

        pub1.publish(arm_pub[0])
        pub2.publish(arm_pub[1])
        pub3.publish(arm_pub[2])
        pub4.publish(arm_pub[3])
        pub5.publish(arm_pub[4])
        pub6.publish(arm_pub[5])
        rate.sleep()

        for i in range(6):
            print("Joint {} angle {} \n".format(i+1,arm_pub[i]))
        

        print("px: py: pz: ",px,py,pz)
        print("x: y: z: ",roll,pitch,yaw) 
           
