#!/usr/bin/env python

# This code provides to control servo - camera
import rospy 
import serial
import time 
import io
import rosparam 

serialMsg  = " "

class Servocamera():
    def __init__(self):
        self.f_letter = 's'  #beginnig of frame
        self.l_letter = 'f'  #ending of frame
        #self.rotate = 0
        self.angle = 0  #Onat'in aci degerlerini yazdirmasiyla duzenlencek.
        self.see_artag = 0
        self.control = " "
        self.first = True
      

    def start(self):

        self.port = rospy.get_param('ServoCamera/ports/servo', 'COM1') 
        self.angle_topic = get_param('ServoCamera/pub_topic_scam/pub_servo_angle', '/servo_angle')
        self.scontrol_topic = get_param('ServoCamera/sub_topic_scam/sub_control', '/servo_control')  #subscribe from artag_search
        self.baudrate = rospy.get_param('ServoCamera/Baudrate/baudrate', 9600)
        self.ser = serial.Serial(self.port, self.baudrate, timeout=1) #bytesize i ogren, buna ekle!
        rate = rospy.Rate(1)

        self.openserial()

        rospy.Subscriber(self.scontrol_topic, String, self.controlSubscriber)
        angle_pub = rospy.Publisher(self.angle_topic, String, queue_size = 10)

    
        while not rospy.is_shutdown():
            if(serialMsg == "s10f"):
                #print("baay")
                self.Writer2()

            if(serialMsg == "s01f"):
                if self.first == True:
                    self.Writer1()
                self.Reader()
            rospy.sleep(0.2)
        rospy.spin()

    def openserial(self):
        try:
            ser.isOpen()
            rospy.loginfo("port is opened.")

        except:
            rospy.loginfo("port is not opened.")

    def Reader(self):
        self.angle = ser.readline() #Onat'in aci degerlerini yazdirmasiyla duzenlencek.
        self.ser.flushInput()
        self.angle_pub.publish(self.angle) #Onat'in aci degerlerini yazdirmasiyla duzenlencek.

    def Writer1(self):

        ser.writelines(f_letter + "0" + "1" + l_letter + "\n")
        self.ser.flushOutput()
        self.first = False

    def Writer2(self):

        ser.writelines(f_letter + "1" + "0" + l_letter + "\n")
        self.ser.flushOutput()


    def controlSubscriber(self,data):
        serialMsg = data.data



if __name__ == '__main__':

    rospy.init_node("serial_servocam")
    try:
        Servocamera()
        print("hello baby!")
    
    except rospy.ROSInterruptException:
        pass

     
    