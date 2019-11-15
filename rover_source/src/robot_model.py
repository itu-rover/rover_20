#!/usr/bin/env python
import sys
import rospy
import moveit_commander
import moveit_msgs.msg
from std_msgs.msg import String
from math import pi

class evren(object): #<3
  def __init__(self):
    super(joint_angles, self).__init__()

    #sub oluncak

    a = {'joint1':/*derece, 'joint2':/*derece...}

    group_name = "manipulator"
    group = moveit_commander.MoveGroupCommander(group_name)

    while not rospy.is_shutdown():

        group.set_joint_value_target()= a

        group.go(a,wait=True)

def main():
  try:
      asd = evren()

  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

if __name__ == '__main__':
  main()
  rospy.spin()
