#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 1-3 are the left side of the rover, 2-4 are the right side of the rover.
# "S + motor_1 + motor_2 + motor_3  + motor_4 + CF"


import rospy
from nmea_msgs.msg import Sentence
import math
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
import geopy.distance 

class autonomous_backup(object):
    def __init__(self):


        self.current_longitude = 0
        self.current_latitude = 0
        self.twist = Twist()
        self.current_yaw = 0
        self.gps_counter = 0
        self.imu_counter = 0
        self.distance = 0             #distance between current point and target point (in meter)


        rospy.init_node('autonomous_backup')
        #rospy.Subscriber("/gps/fix", NavSatFix, self.gps_callback)
        rospy.Subscriber("/imu/data", Imu, self.imu_callback)
        #self.pub=rospy.Publisher("/rover_navigation/cmd_vel", Twist, queue_size=50)
        #self.pub_serial=rospy.Publisher("/rover_serial_topic", String, queue_size=50)
        
        self.main()



    def gps_callback(self, data) :

        self.gps_counter += 1

        latitude_sum = 0
        longitude_sum = 0

        if self.gps_counter < 6 :

        #self.current_longitude = data.longitude              #Positive is east of prime meridian; negative is west.
        #self.current_latitude  = data.latitude               #Positive is north of equator; negative is south.
        
            latitude_sum += data.latitude
            longitude_sum += data.latitude

        if self.gps_counter == 6 :

            self.current_latitude = latitude_sum / 5
            self.current_longitude = longitude_sum / 5
            self.gps_counter = 0 


        print("current_longitude:"+str(self.current_longitude))
        print("current_latitude:"+str(self.current_latitude))

        #R = 6371000 #radius of the Earth, in meter
        #self.x1 = R*math.cos(latitude)*math.cos(longitude)    converts lat/long to 2D coordinates
        #self.y1 = R*math.cos(latitude)*math.sin(longitude)



    def imu_callback(self, data) :

        global roll, pitch, yaw
        
        orientation_q = data.orientation
        orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
        (roll, pitch, yaw) = euler_from_quaternion(orientation_list)

        print(str(yaw))

        self.imu_counter += 1
        yaw_sum = 0

        if self.imu_counter < 6 :
            yaw_sum += yaw

        if self.imu_counter == 6 :

            self.current_yaw = yaw_sum / 5     #in radian, but where is the reference point???

            self.imu_counter = 0 

        
         
        

    """def get_distance(self) :

        coords_1 = (self.current_latitude, self.current_longitude)
        coords_2 = (self.target_latitude, self.target_longitude)

        self.distance = 1000 * geopy.distance.VincentyDistance(coords_1, coords_2).km   #distance between current point and target point (in meter)
"""

    def main(self) :

        rate = rospy.Rate(10)
        
        while not rospy.is_shutdown():

            """self.get_distance()

            distance_status = 3 #indicates bearing status; 1 for far, 2 for middle, 3 for nearest

            if self.distance > 100 : 

                distance_status = 1

            elif self.distance > 10 :

                distance_status = 2


            yaw_error = target_yaw - self.current_yaw

            if distance_status == 3 and yaw_error > pi/36 :

                self.pub_serial.publish("S1010001010100010CF") #Sola tank dönüşü

                  self.twist.angular.z = 0.5
                self.twist.linear.x  = 0
                self.twist.linear.y  = 0
                self.twist.linear.z  = 0
                self.twist.angular.x = 0
                self.twist.angular.y = 0

            elif distance_status == 3 and yaw_error < -pi/36  :

                self.pub_serial.publish("S0010101000101010CF") #Sağa tank dönüşü

                self.twist.angular.z = - 0.5
                self.twist.linear.x  = 0
                self.twist.linear.y  = 0
                self.twist.linear.z  = 0
                self.twist.angular.x = 0
                self.twist.angular.y = 0

            elif distance_status == 3 and yaw_error > -5 and yaw_error < 5 :

                self.pub_serial.publish("S0002000200020002CF") #İleri git


                self.twist.linear.x  = 1
                self.twist.linear.y  = 0
                self.twist.linear.z  = 0
                self.twist.angular.x = 0
                self.twist.angular.y = 0
                self.twist.angular.z = 0

                #if x == self.x1 and y == self.y1  Durma kodu yazılacak.


            elif distance_status == 1 and yaw_error > pi/36 :

                self.pub_serial.publish("S1010001010100010CF") #Sola tank dönüşü

            elif distance_status == 1 and yaw_error < -pi/36 :

                self.pub_serial.publish("S0010101000101010CF") #Sağa tank dönüşü

            elif distance_status == 2 and yaw_error > pi/36 :           

                self.pub_serial.publish("S0000001000000010CF") #Sol dur, sağ ileri

            elif distance_status == 2 and yaw_error < -pi/36 :

                self.pub_serial.publish("S0005000000050000CF") #Sol ileri, sağ dur


            self.pub.publish(self.twist)"""



            rate.sleep()



        #Bulunulan noktanın iki boyutlu düzlemdeki koordinatları elde edilecek.


if __name__ == '__main__':
    autonomous_backup()
