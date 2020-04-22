#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from  rover_control.msg import *
h=0
t=0
rs_gas=0
rate=0

def callbacksensor(data):
    global h, t, rs_gas, rate
    if (data.data != ""):
        sensor=data.data.split(",")
        if(sensor[0]=="S"):
            h=sensor[1]
            t=sensor[2]
            rs_gas=sensor[3]
            rate_=sensor[3]

def main():
  
    rospy.init_node('rover_sensor_sub')
    rospy.Subscriber("/rover_serial_sensor",String, callbacksensor)
    rate = rospy.Rate(1)
    global h, t, rs_gas, rate_
    while  not rospy.is_shutdown():
       
      
      print(str(h))
      delay(5)
    
    rospy.spin()

def delay( value):
    count=0
    rate = rospy.Rate(1)
    while(count<value):
        count=count+1
        rate.sleep()

if __name__ == '__main__':
  try:
    main()
  except rospy.ROSInterruptException:
    pass