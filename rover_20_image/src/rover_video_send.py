#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main(args):
   image_pub = rospy.Publisher("image_topic",Image,queue_size=1)
   bridge = CvBridge()
   bridge.frame_id="camera_link"
   rospy.init_node('image_converter', anonymous=True)
   camera = cv2.VideoCapture(0)
   while not rospy.is_shutdown():

     try:
        (_, frame) = camera.read()
        image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
     except CvBridgeError as e:
        print(e)
  

if __name__ == '__main__':
    main(sys.argv)
