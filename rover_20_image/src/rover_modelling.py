#!/usr/bin/env python
#This is the Modelling Code  for ITU Rover Team
##This code takes pictures with pressing space bar and mark the gps data to their exif's.
###This code is the primary code for modelling and scaling for science task that will be done on another operating system.



import numpy as np
import imutils
import cv2
import rospy
from std_msgs.msg import String
import cv2
import rosparam
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import PIL.Image
import pyexiv2
import fractions
import re
from sensor_msgs.msg import NavSatFix

number = 0
folder_opened = False
currentGps = [None]*2
attribute = rospy.get_param('/RoverModelling/attribute',True)
remote = rospy.get_param('/RoverModelling/remote', True)
remoteControl = ""

def gpsCallback(data):
	global currentGps
	currentGps[0] = data.latitude
	currentGps[1] = data.longitude

def to_deg(value, loc):
	if value < 0:
		loc_value = loc[0]
	elif value > 0:
		loc_value = loc[1]
	else:
		loc_value = ""
	abs_value = abs(value)
	deg =  int(abs_value)
	t1 = (abs_value-deg)*60
	min = int(t1)
	sec = round((t1 - min)* 60, 5)

	return (deg, min, sec, loc_value)

def view_gps_location(file_name, lat, lng):
	"""Adds GPS position as EXIF metadata
	Keyword arguments:
	file_name -- image file 
	lat -- latitude (as float)
	lng -- longitude (as float)
	"""
	lat_deg = to_deg(lat, ["S", "N"])
	lng_deg = to_deg(lng, ["W", "E"])
	
	#print lat_deg
	#print lng_deg
	
	# convert decimal coordinates into degrees, munutes and seconds
	exiv_lat = (pyexiv2.Rational(lat_deg[0]*60+lat_deg[1],60),pyexiv2.Rational(lat_deg[2]*100,6000))
	exiv_lng = (pyexiv2.Rational(lng_deg[0]*60+lng_deg[1],60),pyexiv2.Rational(lng_deg[2]*100,6000))

	exiv_image = pyexiv2.Image(file_name)
	exiv_image.readMetadata()
	exif_keys = exiv_image.exifKeys() 
	
	for key in exif_keys:
		print key, [exiv_image[key]]

def set_gps_location(file_name, lat, lng):
	"""Adds GPS position as EXIF metadata
	Keyword arguments:
	file_name -- image file 
	lat -- latitude (as float)
	lng -- longitude (as float)
	"""	
	global attribute
	lat_deg = to_deg(lat, ["S", "N"])
	lng_deg = to_deg(lng, ["W", "E"])
	
	#print lat_deg
	#print lng_deg
	
	# convert decimal coordinates into degrees, munutes and seconds
	if attribute == False:
		exiv_lat = (pyexiv2.Rational(lat_deg[0]*60+lat_deg[1],60),pyexiv2.Rational(lat_deg[2]*100,6000), pyexiv2.Rational(0, 1))
		exiv_lng = (pyexiv2.Rational(lng_deg[0]*60+lng_deg[1],60),pyexiv2.Rational(lng_deg[2]*100,6000), pyexiv2.Rational(0, 1))
	else:
		exiv_lat = (pyexiv2.Rational(lat_deg[0]*60,60),pyexiv2.Rational(lat_deg[1]*100,100), pyexiv2.Rational(lat_deg[2]*10000, 10000))
		exiv_lng = (pyexiv2.Rational(lng_deg[0]*60,60),pyexiv2.Rational(lng_deg[1]*100,100), pyexiv2.Rational(lng_deg[2]*10000, 10000))

	exiv_image = pyexiv2.ImageMetadata(file_name)
	exiv_image.read()
	exif_keys = exiv_image.exif_keys
	
	exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
	exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
	exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
	exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
	exiv_image["Exif.Image.GPSTag"] = 654
	exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
	exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
	
	exiv_image.write()
	exiv_image.write()

def controlCallback(data):
	global remoteControl
	remoteControl = data.data

def main():
	global number
	global folder_opened
	global currentGps
	global attribute, remote
	global remoteControl
	camera = cv2.VideoCapture(1)
	path_elementary= '/home/cigi/rover_ws/src/rover_18/rover_image/images/'
	fps = 25.0

	while not rospy.is_shutdown():

		#get time
		now=rospy.Time.now() 

		#open folder
		if folder_opened != True:
			path_formed = path_elementary + str(now)
			os.makedirs(path_formed)
			folder_opened = True
			#Create txt
			



		#Read Frame
		(_, frame) = camera.read()
		height, width = frame.shape[:2]
		#frame = frame[0:height,0:int(width*0.5)]
		# Resize and Add Noise
		#frame = imutils.resize(frame, width=1280,height=800)


		cv2.imshow("Frame", frame)
		if remote == False:
			if cv2.waitKey(1) & 0xFF== 32:
				cv2.imwrite(path_formed+'/'+str(number)+'.jpg',frame)
				f = open(path_formed+'/cigi.txt',"a")
				f.write(str(number)+str(currentGps[0])+","+str(currentGps[1]) + "/n")
				number += 1
				f.close()
				if(currentGps[0] != None and currentGps[1] != None):
					set_gps_location(path_formed+'/'+str(number-1)+'.jpg',currentGps[0],currentGps[1])
				else:
					print("currentGps is None")

		else:
			
			if cv2.waitKey(1):
				if remoteControl == "1":
				
					cv2.imwrite(path_formed+'/'+str(number)+'.jpg',frame)
					f = open(path_formed+'/cigi.txt',"a")
					f.write(str(number)+str(currentGps[0])+","+str(currentGps[1]) + "/n")
					number += 1
					f.close()
					if(currentGps[0] != None and currentGps[1] != None):
						set_gps_location(path_formed+'/'+str(number-1)+'.jpg',currentGps[0],currentGps[1])
					else:
						print("currentGps is None")
					remoteControl = ""


	
	camera.release()
	cv2.destroyAllWindows()


if __name__ == '__main__':

	try:
		rospy.init_node('rover_modelling')
		rospy.Subscriber('/gps/fix',NavSatFix,gpsCallback)
		rospy.Subscriber('/rover_modelling/control',String,controlCallback)
		while not rospy.is_shutdown():
			main()
	except rospy.ROSInterruptException:
		pass