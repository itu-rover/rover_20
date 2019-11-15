#!/usr/bin/env python
# -*- coding: utf-8 -*-

#First entered port is always Serial One. Switch ports in case of need.

import rospy
import time
from std_msgs.msg import String
import rosparam

namespace = '[RoverLora_Checkout : ] '



def lora():
    rospy.init_node("rover_lora_checkout")

    global namespace
    global serialMsg

    sensor_pub = rospy.Publisher("/lora/checkout", String, queue_size=10)


    data = 0
    while not rospy.is_shutdown():
        data += 1
        sensor_pub.publish(str(data))
        print(namespace + str(data) + " has sended.")
        rospy.sleep(0.5)







    rospy.spin()




if __name__ == '__main__':
    try:
        lora()
    except rospy.ROSInterruptException:
        pass