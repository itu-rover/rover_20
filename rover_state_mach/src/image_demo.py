#!/usr/bin/env python
## This is the demo code for state_machine.
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray
from status_handler import status_handler
import time

sh = status_handler()

def auto_demo():
    
    pub = rospy.Publisher('/sensor', Int32MultiArray, queue_size=10)
    rospy.init_node('autonomous_demo')
    rate = rospy.Rate(10) # 10hz
    gpsReached = sh.gpsReached
    imageDetected = sh.imageDetected
    imageReached = sh.imageReached
    

    while not rospy.is_shutdown():
        print str(gpsReached) + str(imageReached) + str(imageDetected)

if __name__ == '__main__':
    try:
        
        sh.start()
        while  not rospy.is_shutdown():
            auto_demo()
    except rospy.ROSInterruptException:
        pass
