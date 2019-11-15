#!/usr/bin/env python
import rospy
from rover_state_mach.msg import RoverStateMsg
from std_msgs.msg import String
from sensor_msgs.msg import NavSatFix
from sensor_msgs.msg import Imu
from nav_msgs.msg import Odometry
from actionlib_msgs.msg import GoalStatusArray
import rosparam


class status_handler:
    def __init__(self):
        
        self.namespace = ' [ Rover.StatusHandler ] '

        self.initaliseTimeout = rospy.get_param('RoverSmach/timeouts/initialiseTimeout',600)
        self.readyTimeout = rospy.get_param('RoverSmach/timeouts/readyTimeout',600000)
        self.findImageTimeout = rospy.get_param('RoverSmach/timeouts/findImageTimeout',600000)
        self.reachImageTimeout = rospy.get_param('RoverSmach/timeouts/reachImageTimeout',600000)

        self.gpsReached = False      
        self.imageDetected = False
        self.imageReached = False #False

        	#Parameters for Initalise
        self.gpsWorking = False
        self.imuWorking = True     #!!!!False
        self.encoderWorking = False
        self.allSensorsWorking = False

        	#Parameter for Waypoint
        self.gotWayPoint = False
        

        	#Parameter for Reach Image
        self.goBack = False  #False

        	#Parameter for attribute
        self.movementAttribute = rospy.get_param('RoverSmach/attributes/movementAttribute',0)			#0 for pure navigation, 1 for navigation + image searching.     #0 da calisti

        self.wpStatus = 0
        self.state = 0


        

        


    def start(self):
    	self.wp_topic = rospy.get_param('RoverSmach/sub_topics/sub_waypoint','/waypoint_topic')
    	self.imu_topic = rospy.get_param('RoverSmach/sub_topics/sub_imu','/imu_topic')
    	self.gps_topic = rospy.get_param('RoverSmach/sub_topics/sub_gps','/gps_topic')
    	self.encoder_topic = rospy.get_param('RoverSmach/sub_topics/sub_encoder','/encoder_topic')
    	self.image_detect_topic = rospy.get_param('RoverSmach/sub_topics/sub_image_detect','/px_topic')
    	self.image_reach_topic = rospy.get_param('RoverSmach/sub_topics/sub_image_reach','/image_reach_topic')     #sub_reach_image
    	self.rover_state_topic = rospy.get_param('RoverSmach/pub_topics/pub_rover_state','/rover_state_topic')

    	rospy.Subscriber(self.wp_topic, String, self.waypoint_callback) 						# Listen waypoints
    	rospy.Subscriber(self.gps_topic, NavSatFix, self.gps_callback) 							# Listen Gps
    	rospy.Subscriber(self.imu_topic, Imu, self.imu_callback)								# Listen IMU
    	rospy.Subscriber(self.encoder_topic, Odometry, self.encoder_callback)					# Listen Encoder
    	rospy.Subscriber(self.image_detect_topic, String, self.image_detect_callback) 			# Listen detecting image
    	rospy.Subscriber(self.image_reach_topic, String, self.image_reach_callback)				# Listen reaching image


    	self.state_pub = rospy.Publisher(self.rover_state_topic, RoverStateMsg, queue_size=10)
    	rospy.Subscriber(self.rover_state_topic,RoverStateMsg,self.state_callback)


    def state_callback(self,data):
    	self.state = data.state
    	#print(str(self.state))

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
    	#If GPS module works correct : 
    	if self.currentGps[0] != "0" and self.currentGps[1] != 0:
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

    def image_detect_callback(self,data):
        #UNCOMMENT THIS BLOCK FOR FULL-AUTONOMOUS DRIVING
        '''-------------------------------------------------------------------'''
        self.ballDetected = data.data
        if self.ballDetected != "-":           
            if self.state == 3:                  
                self.imageDetected = True

            self.goBack = False
        else:
            if self.state == 3:
                self.imageDetected = False
            if self.state == 4:
                self.goBack = True
        '''-------------------------------------------------------------------'''

        #UNCOMMENT THIS BLOCK FOR AUTONOMOUS DRIVING WITH FAKE STATE DATA
        '''-------------------------------------------------------------------'''
        #self.ballDetected = data.data
        #if self.self.ballDetected == "1":  
        #    if self.state == True:      
        #        self.imageDetected = True
        #
        #    self.goBack = False
        #else:
        #    if self.state == 3:
        #        self.imageDetected = False
        '''-------------------------------------------------------------------'''
        #DONT FORGET TO SWITCH THE IMAGE_DETECT TOPIC FROM smach_config.yaml


    def image_reach_callback(self,data):
    	self.imageReached = False        #eklendi
        self.ballReached = data.data
    	if self.ballReached == "1":				##TODO: The comprassion have to be right
    		self.imageReached = True
    	elif self.ballReached == "0":
    		self.imageReached = False		
    	"""elif self.ballReached == "2":			#!! GO BACK !!			
    		self.goBack = True"""

    def publishRoverState(self, state_msg):		#Publish the state of Rover
        self.state_pub.publish(state_msg)


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
        self.imageDetected = False
        self.imageReached = False

        	#Parameters for Initalise
        self.gpsWorking = False
        self.imuWorking = False
        self.encoderWorking = False
        self.allSensorsWorking = False

        	#Parameter for Ready
        self.gotWayPoint = False

        	#Parameter for Reach Image
        self.goBack = False
    		




        





    


















