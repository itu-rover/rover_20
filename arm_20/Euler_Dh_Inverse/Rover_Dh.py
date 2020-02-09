#!/usr/bin/env python2
import rospy
import math
from std_msgs.msg import Float64 as F64
from random import randint
from sensor_msgs.msg import Joy

global px,pxi,py,pyi,pz,pzi,w,flag,button,L_1,L_2,L_3,L_4,L_5,L_6,t0,t1,t2,t3,t4,t5,r11,r12,r13,r21,r22,r23,r31,r32,r33
t0=0
t1=0.107913816464
t2=-0.179727353997
t3=-0
t4=0.0718735375331
t5=0.0614454391434
math.pi/2
px=0.9214832735857925
py=-0.04224429255828729
pz=0.13800000000000048
pxi=0.0
pyi=0.0
pzi=0.0
button=0.0
pitch=0
yaw=0
roll=0
pitchi=0.0
yawi=0.0
rolli=0.0

L_1 = 0.14
L_2 = 0.50
L_3 = 0.42
L_4 = -0.11
L_5 = 0
L_6 = 0.1

def callback(data):

    global pxi,pyi,pzi,button,pitch,yaw,roll,L_1,L_2,L_3,L_4,L_5,L_6,t0,t1,t2,t3,t4,t5,rolli,pitchi,yawi
    button=data.buttons[4]
    pxi=data.axes[0]*0.0003
    pyi=data.axes[1]*0.0003
    pzi=data.axes[5]*0.0003
    pitchi=data.axes[3]*0.0003
    yawi=data.axes[2]*0.0003
    rolli=data.axes[4]*0.0003

#px py pz position  x=roll radian angle  y=pitch radian angle z=yaw radian angle
def D_H_calculation(px,py,pz,x,y,z):
    global pxi,pyi,pzi,w,button,L_1,L_2,L_3,L_4,L_5,L_6,t0,t1,t2,t3,t4,t5,r11,r12,r13,r21,r22,r23,r31,r32,r33,rolli,pitchi,yawi
    r11=math.cos(y)*math.cos(z)
    r12=math.cos(z)*math.sin(x)*math.sin(y)-math.cos(x)*math.sin(z)
    r13=math.sin(x)*math.sin(z)+math.cos(x)*math.cos(z)*math.sin(y)
    r21=math.cos(y)*math.sin(z)
    r22=math.cos(x)*math.cos(z)+math.sin(x)*math.sin(y)*math.sin(z)
    r23=math.cos(x)*math.sin(y)*math.sin(z)-math.cos(z)*math.sin(x)
    r31=-math.sin(y)
    r32=math.cos(y)*math.sin(x)
    r33=math.cos(x)*math.cos(y)
    
    #px=math.radians(px)
    #py=math.radians(py)
    #pz=math.radians(pz)
    L_1 = 0.14
    L_2 = 0.50
    L_3 = 0.42
    L_4 = -0.11
    L_5 = 0
    L_6 = 0.1
    #t0=math.atan2(py-L_6*r23,px-L_6*r13)
    #t0=(t0*180)/math.pi
    t0=math.atan((py-L_6*r23)/(px-L_6*r13))
    
    A=math.cos(t0)*(px-L_6*r13)+math.sin(t0)*(py-L_6*r23)
    B=pz-L_6*r33-L_1
    X=2*L_2*L_3
    Y=2*L_2*L_4
    Z=(pow(A,2))+(pow(B,2))-(pow(L_2,2))-(pow(L_3,2))-(pow(L_4,2))
    t2=-math.atan2(Y,X)-math.atan2(math.sqrt(pow(X,2)+pow(Y,2)-pow(Z,2)),Z)

    K_1=(math.cos(t0)*(px-r13*L_6)+math.sin(t0)*(py-r23*L_6))
    K_2=(pz-L_1-r33*L_6)
        
    D=L_3*math.cos(t2)-L_4*math.sin(t2)+L_2

    t1=math.atan2(K_2,K_1)+math.atan2(math.sqrt(pow(K_1,2)+pow(K_2,2)-pow(D,2)),D)

    t3=math.atan((r23*math.cos(t0)-r13*math.sin(t0))/(r33*math.sin(t1+t2)+r13*math.cos(t0)*math.cos(t1+t2)+r23*math.sin(t0)*math.cos(t1+t2)))

    t4=math.acos(-r23*math.sin(t0)*math.sin(t1+t2)-r13*math.cos(t0)*math.sin(t1+t2)+r33*math.cos(t1+t2)) #t4=math.acos(r23*math.sin(t0)*math.sin(t1+t2)+r13*math.cos(t0)*math.sin(t1+t2)-r33*math.cos(t1+t2))

    t5=math.atan((r22 * math.sin(t0) * math.sin(t1+t2) + r12 * math.cos(t0) * math.sin(t1+t2) - r32*math.cos(t1+t2))/(r31 * math.cos(t1+t2)- r11 * math.cos(t0) * math.sin(t1+t2) - r21 * math.sin(t0) * math.sin(t1+t2)))
    
    #t0 = (t0 * 180) / math.pi
    #t1 = (t1 * 180) / math.pi
    #t2 = (t2 * 180) / math.pi
    #t3 = (t3 * 180) / math.pi
    #t4 = (t4 * 180) / math.pi
    #t5 = (t5 * 180) / math.pi
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


        D_H_calculation(px,py,pz,roll,pitch,yaw)

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
        print("r11 r12 r13",r11,r12,r13)
        print("r21 r22 r23",r21,r22,r23)
        print("r31 r32 r33",r31,r32,r33)   





