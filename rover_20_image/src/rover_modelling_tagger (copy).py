#This is the gps tagger code for specific image files for ITU ROVER TEAM.
## Practise code! Not critical...
### All specifies can be found on rover_modelling.py and works livestream.


#!/usr/bin/env python
import numpy as np
import imutils
import cv2
import rospy
from std_msgs.msg import String
import cv2
import rosparam
import os
from PIL import Image
import PIL.Image
from PIL.ExifTags import TAGS, GPSTAGS
import pyexiv2
import fractions
import re


number = 0

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
	
	print lat_deg
	print lng_deg
	
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
	lat_deg = to_deg(lat, ["S", "N"])
	lng_deg = to_deg(lng, ["W", "E"])
	
	print lat_deg
	print lng_deg
	
	lat_deg_sec = str(lat_deg[2]).split('.')
	print(lat_deg_sec[1] + "E")

	# convert decimal coordinates into degrees, munutes and seconds
	exiv_lat = (pyexiv2.Rational(lat_deg[0]*60,60),pyexiv2.Rational(lat_deg[1]*100,100), pyexiv2.Rational(lat_deg[2]*10000000, 10000000))
	exiv_lng = (pyexiv2.Rational(lng_deg[0]*60,60),pyexiv2.Rational(lng_deg[1]*100,100), pyexiv2.Rational(lng_deg[2]*10000000, 10000000))

	exiv_image = pyexiv2.ImageMetadata(file_name)
	exiv_image.read()
	exif_keys = exiv_image.exif_keys
	
	print(str(exiv_lat) + " H")
	exiv_image["Exif.GPSInfo.GPSLatitude"] = exiv_lat
	exiv_image["Exif.GPSInfo.GPSLatitudeRef"] = lat_deg[3]
	exiv_image["Exif.GPSInfo.GPSLongitude"] = exiv_lng
	exiv_image["Exif.GPSInfo.GPSLongitudeRef"] = lng_deg[3]
	exiv_image["Exif.Image.GPSTag"] = 654
	exiv_image["Exif.GPSInfo.GPSMapDatum"] = "WGS-84"
	exiv_image["Exif.GPSInfo.GPSVersionID"] = '2 0 0 0'
	
	exiv_image.write()


def main():
	
	path_elementary= '/home/cigi/rover_ws/src/rover_18/rover_image/images/'


	path_name = path_elementary+'gps.jpg'
	#image = PIL.Image.open(path_name)
	#im = PIL.Image.open(image)

	#exif_data = image._getexif()

	"""exif = {
			PIL.ExifTags.TAGS[k]: v
			for k, v in image._getexif().items()
			if k in PIL.ExifTags.TAGS
	}"""
	set_gps_location(path_name,41.9876532,31.2323)
	while not rospy.is_shutdown():


		now=rospy.Time.now()


if __name__ == '__main__':

	try:
		rospy.init_node('rover_modelling_tagger')
		while not rospy.is_shutdown():

			main()
	except rospy.ROSInterruptException:
		pass