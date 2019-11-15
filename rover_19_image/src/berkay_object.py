#!/usr/bin/env python

from threading import Timer,Thread,Event
import numpy as np
import imutils
import cv2
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
import cv2
import rosparam
from cv_bridge import CvBridge, CvBridgeError
import rosparam

"""
Before use !

You might be need this command for terminal  ->  'sudo rmmod peaq_wmi'

"""
coordinates_x = []
coordinates_y = []
mean_x = None
mean_y = None
pxTopic = rospy.get_param('RoverReachImage/ImageProcessing/pub_pxCoordinates','/px_coordinates')
resize = rospy.get_param('RoverReachImage/ImageProcessing/resize',False)
resize_width = rospy.get_param('RoverReachImage/ImageProcessing/resize_width',1280)
resize_height = rospy.get_param('RoverReachImage/ImageProcessing/resize_height',960)

# Low Pass Filter with a Period = 0.5 seconds
def mean_value(co_x, co_y):
	global mean_x
	global mean_y
	global coordinates_x
	global coordinates_y
	#print("-----------------------")
	#print("Length of arrays before cleaning..\nx,y : {0}--{1}".format(len(co_x),len(co_y)))

	mean_x = float(sum(co_x) / max(len(co_x), 1))
	mean_y = float(sum(co_y) / max(len(co_y), 1))

	#print("Latest Coordinates:{0}--{1}\n ".format(mean_x, mean_y))
	print("Center : {0}--{1}\n ".format(mean_x, mean_y))
	#frees arrays of coordinates
	coordinates_x = []
	coordinates_y = []
	

class LowPassFilter(Thread):
	global coordinates_x
	global coordinates_y
	def __init__(self, event):
		Thread.__init__(self)
		self.stopped = event

	def run(self):
		while not self.stopped.wait(0.1):
			# Call the function if any coordinates detected
			if len(coordinates_y) + len(coordinates_x) != 0:
				mean_value(coordinates_x,coordinates_y)



def main():
	#Coordinates
	global coordinates_x
	global coordinates_y
	coordinates_x = [0]
	coordinates_y = [0]
	global xCoordinate
	global yCoordinate
	global resize
	global resize_width, resize_height
	global mean_x
	global mean_y

	#Start Timer
	stopFlag = Event()
	thread = LowPassFilter(stopFlag)
	thread.start()

	#Video Path
	#video_path = '' #Enter any video path relative to the script file

	#Treshold for Green in BGR Color Space
	greenLower = (40, 58, 77)  # Less accurate -> (29,86,6)  kullanilan(29,50,150)
	greenUpper = (73,255,255)  #kullanilan   (64,255,255)

	#Detection in real time
	camera=cv2.VideoCapture(0)

	bridge = CvBridge()   

	#Detection over video
	#camera = cv2.VideoCapture("video path")
	count=0
	count2=0
	old_x=0
	old_y=0
	difference_x=mean_x - old_x
	difference_y=mean_y - old_y
	old_difference_x=0
	old_difference_y=0
	ball_detected = False

	while not rospy.is_shutdown():#Use this command for detection over a video instead 'True' --> 'camera.isOpened()'

		#Read Frame
		ret, frame = camera.read()
		height, width = frame.shape[:2] #frame = frame[0:height,0:int(width*0.5)]

		# Resize and Add Noise
		if resize == True:
			frame = imutils.resize(frame,width = resize_width, height= resize_height)

		# blurring the frame that's captured
		frame_gau_blur = cv2.GaussianBlur(frame, (3, 3), 1) 

		hsv = cv2.cvtColor(frame_gau_blur, cv2.COLOR_BGR2HSV)
		green_range = cv2.inRange(hsv, greenLower, greenUpper)
		res_green = cv2.bitwise_and(frame_gau_blur,frame_gau_blur, mask=green_range)

		# Masking
		mask = cv2.erode(res_green, None, iterations=2)
		mask = cv2.dilate(mask, None, iterations=3)
		#mask = cv2.GaussianBlur(mask, (5, 5), 0)

		blue_s_gray = cv2.cvtColor(res_green, cv2.COLOR_BGR2GRAY)
		canny_edge = cv2.Canny(blue_s_gray, 200,210)  #100,110
		# applying HoughCircles
		rows=blue_s_gray.shape[0]
		circles = cv2.HoughCircles(canny_edge, cv2.HOUGH_GRADIENT, dp=2, minDist=9, param1=10, param2=5, minRadius=0, maxRadius=0)
		cnts = cv2.findContours(blue_s_gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
		#cnts = imutils.grab_contours(cnts)
		center = None
		

		
		#Execute only at least one contour found
		if len(cnts) > 0 and circles is not None:
			difference_x=mean_x-old_x
			difference_y=mean_y-old_y
			if (-5 <difference_x - old_difference_x< 5 and -5<difference_y - old_difference_y<5):
				count += 1
				count2 = 0

			else:
				print("difference_x=",difference_x) 
				print("old_difference_x=", old_difference_x)
				count = 0
				count2 -= 1
				old_difference_x=difference_x
				old_difference_y=difference_y

				print("count:",count)
				print("count2:",count2)		


			if(count2 < -1):
				ball_detected = False
				count = 0
				count2 = 0
				print("count is become 0")
			elif(count>20):
				count=0
				ball_detected = True
				old_x=mean_x
				old_y=mean_y
				print("count full")
			if (ball_detected is True):
				print("ball_detected True !!")
			else:
				print("ball_detected False !!")
			c = max(cnts, key=cv2.contourArea)
			(x, y), radius = cv2.minEnclosingCircle(c)
			M = cv2.moments(c) 
			print("radius: ",radius)
			if (M["m00"]  != 0 or M["m00"] != 0):
				center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])) 
			else:
				center = (0,0)
			# Select contours with a size bigger than 0.1
			if radius > 0.2 and  ball_detected is True:
				# draw the circle and center
				cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				

				img = Image()
				#height, width = frame.shape[:2]
				img = bridge.cv2_to_imgmsg(frame,"bgr8")
				imagePublisher.publish(img)

				#Hold Coordinates
				coordinates_x.append(center[0])
				coordinates_y.append(center[1])
			
			

				#Free Coordinates if timer is up
				if set == 0:
					coordinates_x = []
					coordinates_y = []
					xCoordinate = 0
					yCoordinate = 0

				frameHeight = frame.shape[0]
				frameWidth = frame.shape[1]
				coordinatePublisher.publish(str(old_x) +","+ str(old_y) + "," + str(frameWidth) + "," + str(frameHeight)+ "," + str(radius))

		else:
			coordinatePublisher.publish("-")
				

		cv2.imshow("Frame", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			stopFlag.set()
			break

	stopFlag.set()
	camera.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':

	try:
		rospy.init_node('rover_detect_ball')        
		coordinatePublisher = rospy.Publisher(pxTopic,String,queue_size = 1)        
		imagePublisher = rospy.Publisher("/image_elevation",Image,queue_size = 10)

		#while not rospy.is_shutdown():
		main()
	except rospy.ROSInterruptException:
		pass
