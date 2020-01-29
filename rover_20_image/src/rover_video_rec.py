#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
def callbackVideo(data):
	global bridge
	video=data
	stream=bridge.imgmsg_to_cv2(video, "bgr8")
	cv2.imshow("Image window", stream)
	cv2.waitKey(1)

def main(args):
   
   rospy.init_node('image_rec', anonymous=True)
   rospy.Subscriber("/image_topic", Image,  callbackVideo)
   rospy.spin()

if __name__ == '__main__':
    main(sys.argv)
