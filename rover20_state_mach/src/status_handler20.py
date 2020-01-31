#!/usr/bin/env python
import rospy
from rover20_state_mach.msg import StateMsg
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from std_msgs.msg import String
from actionlib_msgs.msg import GoalStatusArray
import rosparam


class status_handler:
    def __init__(self):

        self.namespace = ' [ Rover.StatusHandler ] '

        self.initaliseTimeout = rospy.get_param('RoverSmach20/timeouts/initialiseTimeout',600)
        self.readyTimeout = rospy.get_param('RoverSmach20/timeouts/readyTimeout',600000)
        self.findArtagTimeout = rospy.get_param('RoverSmach20/timeouts/findArtagTimeout',600000)
        self.reachArtagTimeout = rospy.get_param('RoverSmach20/timeouts/reachArtagTimeout',600000)
        self.approachTimeout = rospy.get_param('RoverSmach20/timeouts/approachTimeout', 1200000)

        self.gpsReached = False
        self.artagDetected = False
        self.artagReached = False 
        self.passComplete = False #fake
        self.doneApproach = False #fake

        	#Parameters for Initalise
        self.gpsWorking = False
        self.imuWorking = True     #!!!!False
        self.encoderWorking = False
        self.allSensorsWorking = False

        	#Parameter for Waypoint
        self.gotWayPoint = False


        	#Parameter for Reach Artag
        self.goBack = False  #False

        	#Parameter for attribute
        self.movementAttribute = rospy.get_param('RoverSmach20/attributes/movementAttribute',0)			#0 for pure navigation, 1 for navigation + artag searching.     #0 da calisti

        self.wpStatus = 0
        self.state = 0
        self.sc = 1

    def start(self):
    	self.wp_topic = rospy.get_param('RoverSmach20/sub_topics/sub_waypoint','/gps_waypoint_handler/status/gps/fix')
    	self.imu_topic = rospy.get_param('RoverSmach20/sub_topics/sub_imu','/imu/data')
    	self.gps_topic = rospy.get_param('RoverSmach20/sub_topics/sub_gps','/gps/fix')
    	self.encoder_topic = rospy.get_param('RoverSmach20/sub_topics/sub_encoder','/odometry/wheel')
    	self.artag_detect_topic = rospy.get_param('RoverSmach20/sub_topics/sub_artag_detect','/image_detect_topic') 
    	self.artag_reach_topic = rospy.get_param('RoverSmach20/sub_topics/sub_ArTag_reach','/artag_reach_topic')     #sub_reach_artag
    	self.rover_state_topic = rospy.get_param('RoverSmach20/pub_topics/pub_rover_state','/rover_state_topic')
        self.sc_topic = '/stage_counter_topic' #yeni-->stage counter topici 
        self.pass_topic = '/pass_gate_topic' #fake
        self.done_topic = '/done_app_topic'

    	rospy.Subscriber(self.wp_topic, String, self.waypoint_callback) 						# Listen waypoints
    	rospy.Subscriber(self.gps_topic, NavSatFix, self.gps_callback) 							# Listen Gps
    	rospy.Subscriber(self.imu_topic, Imu, self.imu_callback)								# Listen IMU
    	rospy.Subscriber(self.encoder_topic, Odometry, self.encoder_callback)					# Listen Encoder
    	rospy.Subscriber(self.artag_detect_topic, String, self.artag_detect_callback) 			# Listen detecting artag
    	rospy.Subscriber(self.artag_reach_topic, String, self.artag_reach_callback)
        rospy.Subscriber(self.pass_topic, String, self.pass_gate_callback) #fake
        rospy.Subscriber(self.done_topic, String, self.done_approach_callback) #fake
        				# Listen reaching artag


        self.sc_pub = rospy.Publisher(self.sc_topic, String, queue_size = 10) #yeni --> stagecounter topicine publishleniyor.
    	self.state_pub = rospy.Publisher(self.rover_state_topic, StateMsg, queue_size=10)
    	rospy.Subscriber(self.rover_state_topic,StateMsg,self.state_callback)
        rospy.Subscriber(self.sc_topic, String, self.sc_callback)

    def pass_gate_callback(self,data): #fake
        self.pg = data.data
        if(self.pg == "1"):
            self.passComplete = True

    def done_approach_callback(self, data): #fake
        self.d = data.data
        if self.d == "1":
            self.doneApproach = True

    def state_callback(self,data):
    	self.state = data.state
    	#print(str(self.state))

    def sc_callback(self, data):
        self.sc = int(data.data)
        #print(self.sc)

    def waypoint_callback(self,data):								##TODO: Maybe comprassion with old waypoint ??
    	self.wp = data.data

    	#If there is a meaningful waypoint :
    	if self.wp == "1":
    		self.gotWayPoint = True
    		self.gpsReached = False
    	elif self.wp == "2":
    		self.gotWayPoint = False
    		self.gpsReached = True
    	else:
    		self.gotWayPoint = False
    		self.gpsReached = False


    def gps_callback(self,data):									##TODO: Maybe covairance ??
    	self.currentGps = [data.latitude,data.longitude]
    	#print(type(self.currentGps[0]),type(self.currentGps[1]))
    	#If GPS module works correct :
    	if self.currentGps[0] != 0 and self.currentGps[1] != 0:
    		self.gpsWorking = True
    	else:
    		self.gpsWorking = False

        ##### Addition
        #self.gpsWorking = True

    def imu_callback(self,data):									##TODO: Maybe covairance ??
    	self.currentImuOrientation = [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w]
    	self.currentImuAngularV = [data.angular_velocity.x, data.angular_velocity.y, data.angular_velocity.z]
    	self.currentImuLinearA = [data.linear_acceleration.x, data.linear_acceleration.y, data.linear_acceleration.z]
    	#If IMU works correct :
    	if self.currentImuOrientation[0] != '' and self.currentImuOrientation[1] != '':
    		self.imuWorking = True
    	else:
    		self.imuWorking = False


        ##### Addition
        self.imuWorking = True

    def encoder_callback(self,data):								##TODO: Maybe covairance ??
    	self.currentEncoderPose = [data.pose.pose.position.x, data.pose.pose.position.y,data.pose.pose.position.z]
    	#If Encoder works correct :
    	if self.currentEncoderPose[0] != '' and self.currentEncoderPose[1] != '':
    		self.encoderWorking = True
    	else:
    		self.encoderWorking = False


    		self.gpsReached = False

    def artag_detect_callback(self,data):
        #UNCOMMENT THIS BLOCK FOR FULL-AUTONOMOUS DRIVING
        '''-------------------------------------------------------------------'''
        self.ar_Detected = data.data
        if self.ar_Detected != "-":
            if self.state == 3:
                self.artagDetected = True

            self.goBack = False
        else:
            if self.state == 3:
                self.artagDetected = False
            if self.state == 4:
                self.goBack = True
        '''-------------------------------------------------------------------'''

        #UNCOMMENT THIS BLOCK FOR AUTONOMOUS DEMO
        '''-------------------------------------------------------------------'''
        #self.ar_Detected = data.data
        #if self.self.ar_Detected == "1":
        #    if self.state == True:
        #        self.artagDetected = True
        #
        #    self.goBack = False
        #else:
        #    if self.state == 3:
        #        self.artagDetected = False
        '''-------------------------------------------------------------------'''
        #DONT FORGET TO SWITCH THE ARTAG_DETECT TOPIC FROM smach_config.yaml


    def artag_reach_callback(self,data):
    	self.artagReached = False        #eklendi
        self.ar_Reached = data.data
    	if self.ar_Reached == "1":				##TODO: The comprassion have to be right
    		self.artagReached = True
    	elif self.ar_Reached == "0":
    		self.artagReached = False
    	"""elif self.ar_Reached == "2":			#!! GO BACK !!
    		self.goBack = True"""
    def gate_pass_callback(self, data):
        self.gatePass = False 

    def publishRoverState(self, state_msg):		#Publish the state of Rover
        self.state_pub.publish(state_msg)

    def publishRoverSC(self, nowstage):
        self.sc_pub.publish(str(nowstage))

    def checkAllSensors(self):			# Checks sensors for once.

    	if self.encoderWorking == True and self.gpsWorking == True and self.imuWorking == True:
    		self.allSensorsWorking = True


    	elif self.encoderWorking == False and self.gpsWorking == True and self.imuWorking == True:   	##TODO: Decide if encoder is critical here.
    		rospy.logwarn(self.namespace + "All sensors are working except encoder.")
    		self.allSensorsWorking = True

    	else:
    		rospy.logerr(self.namespace + "There is an error!!")
    		self.allSensorsWorking = False


    def deinitialise(self):
    	self.gpsReached = False
        self.artagDetected = False
        self.artagReached = False
        self.passComplete = False #fake
        	#Parameters for Initalise
        self.gpsWorking = False
        self.imuWorking = False
        self.encoderWorking = False
        self.allSensorsWorking = False
        self.doneApproach = False #fake

        	#Parameter for Ready
        self.gotWayPoint = False

        	#Parameter for Reach Artag
        self.goBack = False
