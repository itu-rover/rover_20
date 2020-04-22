#!/usr/bin/env python

# This code provides to control servo - camera
import rospy
import serial
import time
import io
import rosparam
from std_msgs.msg import String


class Servocamera():
	def __init__(self):
		self.f_letter = 's'  #beginnig of frame
		self.l_letter = 'f'  #ending of frame
		#self.rotate = 0
		self.angle = "0"  #Onat'in aci degerlerini yazdirmasiyla duzenlencek.
		self.see_artag = 0
		self.control = " "
		#self.first = True
		self.servo_rotating = False
		self.serialMsg = " "
		self.donedone = None
		self.start()



	def start(self):

		self.port = rospy.get_param('ServoCamera/ports/servoport', '/dev/ttyUSB2')
		self.angle_topic = rospy.get_param('ServoCamera/pub_topic_scam/pub_servo_angle', '/servo_angle')
		self.scontrol_topic = rospy.get_param('ServoCamera/sub_topic_scam/sub_control', '/servo_control')  #subscribe from artag_search
		self.baudrate = rospy.get_param('ServoCamera/Baudrate/baudrate', 9600)
		self.servodone_topic = rospy.get_param('ServoCamera/pub_topic_scam/pub_servodone', '/servodone')
		#time.sleep(2)
		#self.ser = serial.Serial(self.port, self.baudrate, timeout=1) #bytesize i ogren, buna ekle!
		rate = rospy.Rate(30)
		self.openserial()
		self.angle_pub = rospy.Publisher(self.angle_topic, String, queue_size = 10)
		self.pub_notrotate = rospy.Publisher('/servodone', String, queue_size=10)

		

		while not rospy.is_shutdown():
			self.serialMsg = " "
			self.angle_pub.publish(self.angle)
			rospy.Subscriber(self.scontrol_topic, String, self.controlSubscriber)
			#print(self.servo_rotating)
			#print(self.serialMsg)
			time.sleep(1)
			#self.control = self.ser.readline()
			#self.ser.flushInput()
			#print("status:", self.control, "serialMsg:", self.serialMsg, "servo_rotating:", self.servo_rotating)
			self.done_servo_rotation()

			if(self.serialMsg == "s10f" and self.servo_rotating is False):
				#print("s10f done")
				self.start_servo()
				print("started:" )
				self.servo_rotating = True

			if(self.serialMsg == "s01f"): #and self.servo_rotating is True): and self.servo_rotating is True
				#if self.first == True:
				self.stop_servo()
				#time.sleep(5)
				print("stopped")
				self.servo_rotating = False
				for i in range(100):
					self.take_angle()
				#angle_pub = rospy.Publisher(self.angle_topic, String, queue_size = 10)
				continue
			if(self.serialMsg == "s00f"):
				self.ser.flushInput()
				self.ser.flushOutput()
				self.ser.writelines(self.f_letter + "0" + "0" + self.l_letter + "\n")

			rospy.sleep(0.2)

		rospy.spin()

	def openserial(self):
		print("jbcj")
		#try:
		self.ser = serial.Serial(self.port, self.baudrate, timeout=1) #bytesize i ogren, buna ekle!
		#self.ser.open() #
		#self.ser.isOpen()
		rospy.loginfo("port is opened.")
		
		'''except IOError:
			rospy.loginfo("port is not opened.")
			self.ser.close()
			self.ser.open()
			self.ser.isOpen()
			rospy.loginfo("port was already open, was closed and opened again!")
		
	'''
		
	def take_angle(self):
		self.angle = self.ser.readline() 
		#self.ser.flushInput()
		print("angleof servo:", self.angle)
		self.angle_pub.publish(self.angle)
		if self.angle == None:
			self.angle_pub.publish("0")


	def done_servo_rotation (self):
		self.notrotating = self.ser.readline()
		#self.ser.flushOutput()
		print("status:", self.notrotating, "serialMsg:", self.serialMsg, "servo_rotating:", self.servo_rotating)

		if self.notrotating == "1\r\n":
			self.pub_notrotate.publish("1")
			self.servo_rotating = False
		else:
			self.pub_notrotate.publish("0")

	def stop_servo(self):
		#self.ser.flushInput()
		self.ser.writelines(self.f_letter + "0" + "1" + self.l_letter + "\n")
		
		#self.ser.flushInput()
		#self.first = False
		#rospy.loginfo('writer 1')

	def start_servo(self): 
		#self.ser.flushInput()
		self.ser.writelines(self.f_letter + "1" + "0" + self.l_letter + "\n")
		#rospy.loginfo('10 basildi')
		#rospy.loginfo("while ici writer iki")
		print("nbckjgn")

	def controlSubscriber(self,data):
		self.serialMsg = data.data



if __name__ == '__main__':
	rospy.init_node("serial_servocam")
	try:
		Servocamera()
		print("hello baby!")

	except rospy.ROSInterruptException:
		pass


