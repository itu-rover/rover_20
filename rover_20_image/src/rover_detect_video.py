#!/usr/bin/env python
import numpy as np
import imutils
import cv2
import rospy
from std_msgs.msg import String

video_path = '/home/cigi/rover_ws/src/rover_18/rover_image/include/rover_image/1.mp4';

greenLower = (29, 86, 6)#29,86,6
greenUpper = (64, 255, 255)

camera = cv2.VideoCapture(video_path)

def main():
	while (camera.isOpened()) and not rospy.is_shutdown():

		(_, frame) = camera.read()

		frame = imutils.resize(frame, width=1200)
		#frame = cv2.GaussianBlur(frame, (11, 11), 0)
	#Blur eklenmeli eklenmeli mi hala emin degilim
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

		# construct a mask for the color "green", then perform
		# a series of dilations and erosions to remove any small
		# blobs left in the mask
		mask = cv2.inRange(hsv, greenLower, greenUpper)
		mask = cv2.erode(mask, None, iterations=3)
		mask = cv2.dilate(mask, None, iterations=2)

		# find contours in the mask and initialize the current
		# (x, y) center of the ball
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)[-2]
		center = None
		
		# only proceed if at least one contour was found
		if len(cnts) > 0:
			# find the largest contour in the mask, then use
			# it to compute the minimum enclosing circle and
			# centroid
			c = max(cnts, key=cv2.contourArea)
			((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			#print("Center x:{0} and y:{1}\n ".format(x,y))
			# only proceed if the radius meets a minimum size
			if radius > 0.5:
				# draw the circle and centroid on the frame,
				cv2.circle(frame, (int(x), int(y)), int(radius),
					(0, 255, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)

			coordinatePublisher.publish(str(x) +","+ str(y))

		cv2.imshow("Frame", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
	        	break


	camera.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':

	try:
		rospy.init_node('rover_detect_video')
		coordinatePublisher = rospy.Publisher('/pixel_coordinates',String,queue_size = 100)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass
