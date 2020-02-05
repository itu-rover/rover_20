#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This node is used only for real lidar with elevation mapping 
import math
from math import sin,cos, pi
import rospy
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3,PoseWithCovarianceStamped
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix, Imu, PointCloud2
from geographic_msgs.msg import WayPoint, GeoPoint



class Localization(object):
    def __init__(self):
        rospy.init_node('rover_fake_point_cloud')

  
        self.current_time =  rospy.Time.now()
        self.last_time =  rospy.Time.now()
        self.Point=PointCloud2()
        self.pose_pub = rospy.Publisher('/rover_serial_encoder',String, queue_size = 10)
        self.controller()
       
     
 
    def callback(self,data):
       self.Point=data
       
      
    def controller(self):

        #rospy.Subscriber('/cloud', PointCloud2, self.callback)

        msg = ""
        x = 1344
        self.rate = rospy.Rate(5) #10 Hz
        while not rospy.is_shutdown():
            msg = "S"+ str(x)+",911116,"+str(x)+",11125F"
            self.current_time = rospy.Time.now()
            self.Point.header.stamp=self.current_time
            self.pose_pub.publish(msg)
            x += 2
            self.rate.sleep()

            
             

if __name__ == '__main__':
    Localization()

