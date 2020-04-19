#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Used as a backup plan for autonomous driving. Subs IMU and GPS data only. Draws a line between current point and target point, makes rover follow that line with a tolerance of +/- 5 degrees. Reaches target point with 0.5 m error. 

# 1-3 are the left side of the rover, 2-4 are the right side of the rover.
# "S + motor_1 + motor_2 + motor_3  + motor_4 + CF"
#Last update: 01.05.2019


import rospy
from nmea_msgs.msg import Sentence
import math
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from sensor_msgs.msg import NavSatFix
import geopy.distance 
from std_msgs.msg import String

class autonomous_backup(object):
	def __init__(self):


		self.current_longitude = 0
		self.current_latitude  = 0
		self.twist             = Twist()
		self.current_yaw       = 0
		self.gps_counter       = 0
		self.imu_counter       = 0
		self.distance          = 0         #distance between current point and target point (in meter)
		self.target_latitude   = 0
		self.yaw_sum           = 0
		self.latitude_sum      = 0
		self.longitude_sum     = 0
		self.imu_offset        = 0         #Our IMU (Bosch BNO055) gives zero yaw angle when facing east (determined with imu_reader.py).      

		self.twist.angular.z = 0
		self.twist.linear.x  = 0
		self.twist.linear.y  = 0
		self.twist.linear.z  = 0
		self.twist.angular.x = 0
		self.twist.angular.y = 0



		rospy.init_node('autonomous_backup')
		rospy.Subscriber("/gps/fix", NavSatFix, self.gps_callback) #/gps/fix for driving in real life, /navsat/fix for husky in gazebo
		rospy.Subscriber("/imu/data", Imu, self.imu_callback)
		self.pub=rospy.Publisher("/cmd_vel", Twist, queue_size = 50)
		#self.pub_serial=rospy.Publisher("/rover_serial_topic", String, queue_size=50)
		
		self.main()



	def gps_callback(self, data) : #calculates average of 5 consecutive latitude and longitude data

		self.gps_counter += 1

		if self.gps_counter < 6 :

		#self.current_longitude = data.longitude              #Positive is east of prime meridian; negative is west.
		#self.current_latitude  = data.latitude               #Positive is north of equator; negative is south.
		
			self.latitude_sum  += data.latitude
			self.longitude_sum += data.longitude

		if self.gps_counter == 6 :

			self.current_latitude  = self.latitude_sum / 5
			self.current_longitude = self.longitude_sum / 5
			self.gps_counter   = 0 
			self.latitude_sum  = 0
			self.longitude_sum = 0

		#print("current_longitude:"+str(self.current_longitude))
		#print("current_latitude:"+str(self.current_latitude))

		#R = 6371000 #radius of the Earth, in meter
		#self.x1 = R*math.cos(latitude)*math.cos(longitude)    converts lat/long to 2D coordinates
		#self.y1 = R*math.cos(latitude)*math.sin(longitude)



	def imu_callback(self, data) :   #calculates average of 5 consecutive yaw angle data

		global roll, pitch, yaw
		
		orientation_q = data.orientation
		orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
		(roll, pitch, yaw) = euler_from_quaternion(orientation_list)     #yaw is between -pi and pi.

		#print("yaw: "+str(yaw))
		yaw -=  math.pi #((self.imu_offset-90)/90)*math.pi

		if yaw > math.pi:
			yaw -= math.pi*2
		if yaw < -math.pi:
			yaw += math.pi*2

		if yaw > 0 and yaw < math.pi :      #Comment this if-elif block when driving rover in real life.

			yaw += math.pi/2                #Uncomment this if-elif block to change IMU yaw angle reference from north to east when using husky in Gazebo.

		elif yaw < 0 and yaw > -math.pi :

			yaw += math.pi/2

		self.imu_counter += 1
		

		if self.imu_counter < 6 :
			
			self.yaw_sum += yaw

		if self.imu_counter == 6 :

			self.current_yaw = self.yaw_sum / 5    

			self.imu_counter = 0

			self.yaw_sum = 0 

		
		 
		
	def get_distance(self) :

		coords_1 = (self.current_latitude, self.current_longitude)
		coords_2 = (self.target_latitude, self.target_longitude)

		self.distance = 1000 * geopy.distance.VincentyDistance(coords_1, coords_2).km   #distance between current point and target point (in meter)
		print("self.distance    :"+str(self.distance))

	

	def main(self) :

		new_goal = 1

		while new_goal == 1 :

			print("Enter GPS coordinates (latitude longitude) of target point.")
			print("Enter latitude.")
			self.target_latitude = float(raw_input())
			print("Enter longitude.")
			self.target_longitude = float(raw_input())

			
			rate = rospy.Rate(1) #10

			goal_status = False
			
			while not rospy.is_shutdown() and goal_status == False :

				if self.current_longitude == self.target_longitude and self.target_latitude > self.current_latitude :

					target_yaw = math.pi/2

				elif self.current_longitude == self.target_longitude and self.target_latitude < self.current_latitude :

					target_yaw = -math.pi/2 

				else :

					target_slope = (self.target_latitude - self.current_latitude)/(self.target_longitude - self.current_longitude)  
					target_yaw = math.atan(target_slope)   #in radian, starting from horizontal axis

					if target_yaw > 0 and self.target_latitude < self.current_latitude :  # atan > 0 in both 1st and 3rd coordinate region

						target_yaw += math.pi

					if target_yaw < 0 and self.target_latitude > self.current_latitude :  # atan < 0 in both 2nd and 4th coordinate region

						target_yaw -= math.pi

				#Should the lines above be inside or outside of while loop?

				self.get_distance()

				distance_status = 4 #indicates bearing status; 1 for far, 2 for middle, 3 for near, 4 for in 4 meter-radius

				if self.distance > 20 : 

					distance_status = 1

				elif self.distance > 7 :

					distance_status = 2

				elif self.distance > 4 :

					distance_status = 3

				yaw_error = target_yaw - self.current_yaw

				while abs(yaw_error) > math.pi :      #changes yaw_error range to [-pi,pi]

					yaw_error += -1*get_sign(yaw_error)*2*math.pi  
				
				#print(self.imu_counter)
				#print("yaw_error        :"+str(yaw_error))
				#print("current_yaw      :"+str(self.current_yaw))
				#print("distance_status  :"+str(distance_status))
				#print("current_latitude :"+str(self.current_latitude))
				#print("current_longitude:"+str(self.current_longitude))
				#print("target_latitude  :"+str(self.target_latitude))
				#print("target_longitude :"+str(self.target_longitude))

				if distance_status == 3 and yaw_error > math.pi/9 :

					#self.pub_serial.publish("S1010001010100010CF") #Sola tank dönüşü

					self.twist.angular.z = 0.4
					self.twist.linear.x  = 0
					
				

				elif distance_status == 3 and yaw_error < -math.pi/9  :

					#self.pub_serial.publish("S0010101000101010CF") #Sağa tank dönüşü

					self.twist.angular.z = - 0.4
					self.twist.linear.x  = 0
					
					

				elif distance_status == 3 and yaw_error > -math.pi/9 and yaw_error < math.pi/9 :

					#self.pub_serial.publish("S0002000200020002CF") #İleri git


					self.twist.linear.x  = 1
					self.twist.angular.z = 0


					
					

				elif distance_status == 1 and yaw_error > math.pi/9 :

					#self.pub_serial.publish("S1010001010100010CF") #Sola tank dönüşü (veya dönerek mi ilerlesin???)

					self.twist.angular.z = 0.5
					self.twist.linear.x  = 0
					
					

				elif distance_status == 1 and yaw_error < -math.pi/9 :

					#self.pub_serial.publish("S0010101000101010CF") #Sağa tank dönüşü (veya dönerek mi ilerlesin???)

					self.twist.angular.z = - 0.5
					self.twist.linear.x  = 0
					

					

				elif distance_status == 1 and yaw_error > -math.pi/9 and yaw_error < math.pi/9 :

					#self.pub_serial.publish("S0010001000100010CF") #İleri git

					self.twist.angular.z = 0
					self.twist.linear.x  = 1
					
					
				elif distance_status == 2 and yaw_error > math.pi/9 :			

					#self.pub_serial.publish("S0000001000000010CF") #Sol dur, sağ ileri

					self.twist.angular.z = 0.5
					self.twist.linear.x  = 1
					

				elif distance_status == 2 and yaw_error < -math.pi/9 :

					#self.pub_serial.publish("S0005000000050000CF") #Sol ileri, sağ dur

					self.twist.angular.z = - 0.5
					self.twist.linear.x  = 1
					

				elif distance_status == 2 and yaw_error > -math.pi/9 and yaw_error < math.pi/9 :

					#self.pub_serial.publish("S0010001000100010CF") #İleri git

					self.twist.angular.z = 0
					self.twist.linear.x  = 1
					

				elif distance_status == 4 :

					if self.distance > 0.5 :

						#self.pub_serial.publish("S0000000000000000CF")

						self.twist.angular.z = 0
						self.twist.linear.x  = 0

						self.pub.publish(self.twist)

						print("adim1")
					

						#self.gps_counter = 0     #or add sleep() ???
						#self.latitude_sum = 0
						#self.longitude_sum = 0

						print("yaw_error_status_4:"+str(yaw_error))

						if yaw_error > math.pi/9 :

							#self.pub_serial.publish("S1010001010100010CF") #Sola tank dönüşü

							self.twist.angular.z = 0.5
							self.twist.linear.x  = 0

					
						elif yaw_error < -math.pi/9 :

							#self.pub_serial.publish("S0010101000101010CF") #Sağa tank dönüşü

							self.twist.angular.z = -0.5
							self.twist.linear.x  = 0
					
							
						elif  yaw_error > -math.pi/9 and yaw_error < math.pi/9 :

							#self.pub_serial.publish("S0001000100010001CF") #İleri git

							self.twist.angular.z = 0
							self.twist.linear.x  = 0.3

						
					else :
					
						#self.pub_serial.publish("S0000000000000000CF")

						self.twist.angular.z = 0
						self.twist.linear.x  = 0

						print("adim2")
						
						
						goal_status = True
						print("Goal reached")


				self.pub.publish(self.twist)

			rate.sleep()

			if goal_status == True :

				print("Enter 1 to send new goal, 0 to exit.")
				new_goal = int(raw_input())



			



		#Bulunulan noktanın iki boyutlu düzlemdeki koordinatları elde edilecek.
def get_sign(number) :

	if number < 0 :

		return -1

	elif number > 0 :

		return 1

	else :

		return 0

if __name__ == '__main__':
	autonomous_backup()
