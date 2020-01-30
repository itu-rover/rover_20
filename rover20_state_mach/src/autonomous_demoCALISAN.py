#!/usr/bin/env python
## This is the demo code for state_machine.
import rospy
from std_msgs.msg import String
from status_handler import status_handler
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
from actionlib_msgs.msg import GoalStatus
import time
import rosparam

sh = status_handler()

def auto_demo():
    rospy.init_node('autonomous_demo')

    #Requirements 
    pub1 = rospy.Publisher('/gps/fix', NavSatFix, queue_size =10)
    pub2 = rospy.Publisher('/imu/data', Imu ,queue_size = 10)
    pub3 = rospy.Publisher('/odometry/wheel', Odometry, queue_size = 10)
    pub4 = rospy.Publisher('/gps_waypoint_handler/status', String, queue_size = 10)

    #Autonomous movement
    #pub5 = rospy.Publisher('/move_base/status',GoalStatusArray,queue_size=10)
    
    #Image Detect
    pub6 = rospy.Publisher('/image_detect_topic',String,queue_size=10)

    #Image Reach
    pub7 = rospy.Publisher('/image_reach_topic',String,queue_size=10)
    rate = rospy.Rate(10) # 10hz
    count = 0

    while not rospy.is_shutdown():
        print("0: All sensors are good.")
        print("1: All sensors except encoder are good.")
        print("2: Damaged Sensors")
        print("3: Got Waypoint")
        print("4: Did not get any waypoint")
        print("5: Reached to way point")
        print("6: Did not Reached to way point")
        print("7: Detected Ar Tag")
        print("8: Did not detect Ar Tag")
        print("9: Reached Ar Tag")
        print("10: Did not reached Ar Tag")

        imuMsg = Imu()
        imuMsg.orientation.x = 5
        imuMsg.orientation.y = 5
        gpsMsg = NavSatFix()
        gpsMsg.latitude = 5
        gpsMsg.longitude = 5
        encoderMsg = Odometry()
        encoderMsg.pose.pose.position.x = 5
        encoderMsg.pose.pose.position.y = 5
        
        wpStatusMsgLow = GoalStatus()
        wpStatusMsgLow.status = 3
        wpStatusArray =[]
        wpStatusArray.append(wpStatusMsgLow)
        wpStatusMsg = GoalStatusArray()
        wpStatusMsg.status_list = wpStatusArray

        userInput = raw_input()
        if userInput == "0":   #All sensors are good.

            pub1.publish(gpsMsg)
            pub2.publish(imuMsg)
            pub3.publish(encoderMsg)
            
        elif userInput == "1":  # All sensors except encoder are good.
            pub1.publish(gpsMsg)
            pub2.publish(imuMsg)
            #pub3.publish("0")

        elif userInput == "2":   #Damaged Sensors
            pub1.publish(gpsMsg)
            #pub2.publish("0")
            pub3.publish(encoderMsg)
            
        elif userInput == "3":  # Got Waypoint
            pub4.publish("1")

        #elif userInput == "4":  #Did not get any waypoint
            #pub4.publish("0")

        elif userInput == "5":  #Reached to way point
            #pub5.publish(wpStatusMsg)
            pub4.publish("2")
            

        #elif userInput == "6":  #Did not reached to way point
            #pub5.publish("0")


        elif userInput == "7":  #Detected Image
            pub6.publish("1")

        elif userInput == "8":  #Did not Detect Ar Tag
            pub6.publish("0")

        elif userInput == "9":  #Reached Ar Tag
            pub7.publish("1")

        elif userInput == "10": #Did not reached image
            pub7.publish("0")
        else:
            print("Invalid entry")


        rate.sleep()

if __name__ == '__main__':
    try:
        
        sh.start()
        while  not rospy.is_shutdown():
            auto_demo()
    except rospy.ROSInterruptException:
        pass
