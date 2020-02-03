#!/usr/bin/env python


### THIS IS THE STATE MACHINE FOR ITU ROVER


import rospy
import smach
import smach_ros
from std_msgs.msg import String
from status_handler20 import status_handler
from rover20_state_mach.msg import StateMsg
from diagnostic_msgs.msg import DiagnosticArray
import rosparam
import time

_namespace = '[RoverStateMachine ] '
status_handler = status_handler()
#scMsg = status_handler.sc

####################################################################################################################################################
# First State of the ITU Rover
## Checksgps, imu, encoder datas through status_handler
### If they are all working correct, passes to Ready State.
#### Encoder sensor is not critical here.

class INITIALISE(smach.State):

    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['REPEAT', 'FAIL', 'SUCCESS'])
        self.initaliseTimeout = status_handler.initaliseTimeout
        self.timeoutCounter = status_handler.initaliseTimeout
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()
        #self.scMsg = status_handler.sc

    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On Initialise state')

        self.stateMsg.state = self.stateMsg.INITIALISE

        status_handler.publishRoverState(self.stateMsg)
        status_handler.publishRoverSC(status_handler.sc)
        #print(self.scMsg)

        self.gpsWorking = status_handler.gpsWorking                                                   # Necessary parameters to go to READY state
        self.imuWorking = status_handler.imuWorking
        self.encoderWorking = status_handler.encoderWorking

        if self.gpsWorking == True and self.imuWorking == True and self.encoderWorking == True:         # Check all necessary parameters.
            rospy.loginfo(_namespace + "All localization sensors are working good...")
            self.timeoutCounter = 0
            return 'SUCCESS'                                                                            ## TODO : Criticize if encoder is critical here.

        elif self.gpsWorking == True and self.imuWorking == True and self.encoderWorking != True:       # Check all necessary parameters except encoder
            rospy.loginfo(_namespace + "All localization sensors are working good except encoder...")
            self.timeoutCounter = 0
            return 'SUCCESS'

        else:                                                                                           # Count timeout.
            self.timeoutCounter += 1

        if self.timeoutCounter == self.initaliseTimeout:                                                # If Timeout counter has reached the limit.
            self.timeoutCounter = 0
            return 'FAIL'

        #print("Gps working {}\nImu working {}\n\n".format(self.gpsWorking,self.imuWorking))

        rospy.sleep(0.1)
        return 'REPEAT'

######################################################################################################################################################
# Checks if there is an meaningful waypoint.
## After waypoint-check, checks once if the sensors are still working.
### If sensors are still working correct, moves to GPS State.
#### If there is an error on sensors, switches to ERROR State.

class READY(smach.State):

    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['TO_GPS', 'FAIL','REPEAT'])
        self.readyTimeout = status_handler.readyTimeout
        self.timeoutCounter = 0
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()

    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On Ready State')

        self.stateMsg.state = self.stateMsg.READY
        status_handler.publishRoverState(self.stateMsg)

        self.gotWayPoint = status_handler.gotWayPoint



        if self.gotWayPoint == True:

            status_handler.checkAllSensors()                                                      #Check All Sensors For Once ##TODO: Criticize if it is neccesary
            self.allSensorsWorking = status_handler.allSensorsWorking

            if self.allSensorsWorking == True:
                rospy.loginfo(_namespace + "Got new waypoint. Switching to GPS state.")
                self.timeoutCounter = 0
                return 'TO_GPS'

            else:
                return 'FAIL'

        else:
            self.timeoutCounter += 1

        if self.timeoutCounter == self.readyTimeout:
            rospy.loginfo("Waited too long for waypoint ...")
            self.timeoutCounter = 0
            return 'FAIL'

        rospy.sleep(0.1)
        return 'REPEAT'
#########################################################################################################################################################
#Checks the Attribute parameter
## If it is 0, rover navigates without searching ball, if it is 1, vice versa.
### Checks if the rover reached wp, and detected the ball

class REACH_GPS(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS','IMAGE_INTERRUPT', 'FAIL', 'REPEAT', 'SUCCES12'])
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()
        #self.scMsg = rospy.Subscriber

    def execute(self, userdata):
        rospy.loginfo(_namespace + "On Reach GPS State")

        self.stateMsg.state = self.stateMsg.REACH_GPS
        status_handler.publishRoverState(self.stateMsg)

        self.gpsReached = status_handler.gpsReached
        self.artagDetected = status_handler.artagDetected

        self.movementAttribute = status_handler.movementAttribute

        if self.movementAttribute == 0: #muhtemelen test case
            if self.gpsReached == True:
                rospy.loginfo(_namespace + "Reached to GPS, moving to FIND_ARTAG state.")
                return 'SUCCESS'   #muhtemelen test case

        elif self.movementAttribute == 1:
            if self.scMsg == 1 or self.scMsg == 2 :
                if self.gpsReached == True:
                    rospy.loginfo(_namespace + "Reached to Gps, moving to DEINITIALISE state.")
                    return 'SUCCES12'

            elif self.gpsReached == False and self.artagDetected == True:
                rospy.loginfo(_namespace + "Detected the ARTAG, moving to REACH_ARTAG state.")
                return 'IMAGE_INTERRUPT'

            elif self.gpsReached == True and self.artagDetected == False:
                rospy.loginfo(_namespace + "Reached to Gps, moving to FIND_ARTAG state.")
                return 'SUCCESS'

            elif self.gpsReached == True and self.artagDetected == True:
                rospy.loginfo(_namespace + "Reached to Gps, Detected the ARTAG, moving to REACH_ARTAG state.")
                return 'IMAGE_INTERRUPT'


        rospy.sleep(0.1)
        return 'REPEAT'
##############################################################################################################################################################
# Checks if image detected.
## That's all.
class FIND_ARTAG(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS', 'FAIL', 'REPEAT', 'GO_APPROACH'])
        self.findArtagTimeout = status_handler.findArtagTimeout
        self.timeoutCounter = 0
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()
        self.goBack = status_handler.goBack
        self.goBack = False
        #self.scMsg = rospy.Subscriber



    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On Find Artag State')

        self.stateMsg.state = self.stateMsg.FIND_ARTAG
        status_handler.publishRoverState(self.stateMsg)
        self.artagDetected = status_handler.artagDetected
        print(str(self.artagDetected))
        if self.artagDetected == True:
            #if(self.scMsg >= 4):
            rospy.loginfo(_namespace + "Artag has detected, moving to APPROACH state")
            self.timeoutCounter = 0
            self.artagDetected = False  #??
            return 'GO_APPROACH'

            """
            else :					#elif(self.scMsg == 3):
                rospy.loginfo(_namespace + "Artag has detected, moving to REACH_ARTAG state")
                self.timeoutCounter = 0
                self.artagDetected = False  #??
                return 'SUCCESS'
            """
        else:
            self.timeoutCounter += 1

        if self.timeoutCounter == self.findArtagTimeout:
            rospy.loginfo(_namespace + "Artag is still not detected, get your shit together.")
            self.timeoutCounter = 0
            return 'RETURN'


        rospy.sleep(0.1)
        return 'REPEAT'
###########################################################################################################################################################

class APPROACH(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS', 'FAIL', 'REPEAT'])
        self.approachTimeout = status_handler.approachTimeout
        self.timeoutCounter = 0
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()
        self.goBack = status_handler.goBack
        self.goBack = False
        #self.goapp = False




    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On APPROACH State')

        self.stateMsg.state = self.stateMsg.APPROACH
        status_handler.publishRoverState(self.stateMsg)
        self.doneApproach = status_handler.doneApproach
        #if self.gatePass == True:
        #if(self.scMsg >= 4):
        if self.doneApproach == True: #fake
            rospy.loginfo(_namespace + "Artag has detected, moving to DEINITIALISE state")
            self.timeoutCounter = 0
            return 'SUCCESS'

        self.timeoutCounter += 1

        if self.timeoutCounter == self.approachTimeout:
            rospy.loginfo(_namespace + "Artag is still not detected, get your shit together.")
            self.timeoutCounter = 0
            return 'RETURN'


        rospy.sleep(0.1)
        return 'REPEAT'

class PASS_GATE(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS', 'FAIL','REPEAT_APPROACH'])
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()

    def execute(self, userdata):
        rospy.loginfo(_namespace + "On PASS_GATE State")

        self.stateMsg.state = self.stateMsg.PASS_GATE
        status_handler.publishRoverState(self.stateMsg)
        self.control_dir = status_handler.control_dir
        self.passComplete = status_handler.passComplete #fake

        if self.passComplete == True: #fake
               rospy.loginfo(_namespace + "Pass through the gate, moving to DEINITIALISE state.")
               return 'SUCCESS'

        if self.control_dir == False:
            rospy.loginfo(_namespace + " Pass through the gate, moving to DEINITIALISE state.")
            self.timeoutCounter = 0
            return 'SUCCESS'


        rospy.sleep(0.1)
        return 'REPEAT_APPROACH'

###########################################################################################################################################################


class REACH_ARTAG(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS', 'FAIL', 'REPEAT','BACK'])
        self.reachArtagTimeout = status_handler.reachArtagTimeout
        self.timeoutCounter = 0
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()

    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On Reach Artag State')

        self.stateMsg.state = self.stateMsg.REACH_ARTAG
        status_handler.publishRoverState(self.stateMsg)



        self.artagReached = status_handler.artagReached
        self.goBack = status_handler.goBack

        if self.scMsg == 3 :
            if self.artagReached == True:
                rospy.loginfo(_namespace + "Reached The Ball !!")
                self.timeoutCounter = 0
                self.artagReached = False    #eklendi
                return 'SUCCESS'
            else:
                self.timeoutCounter += 1

        if self.timeoutCounter == self.reachArtagTimeout:
            rospy.loginfo(_namespace + "Ball is still not reached, get your shit together.")
            status_handler.checkAllSensors()                                                      #Check All Sensors For Once ##TODO: Criticize if it is neccesary
            self.allSensorsWorking = status_handler.allSensorsWorking
            if self.allSensorsWorking == True:
                self.timeoutCounter = 0
                return 'REPEAT'     #RETURN
            else:
                self.timeoutCounter = 0
                return 'FAIL'
        print(str(self.goBack))
        if self.goBack == True:
            rospy.loginfo(_namespace + "Going back to last waypoint and searching for the ball.")
            self.timeoutCounter = 0
            return 'BACK'                                                                              ## !! TO DO : send waypoint here !!



        rospy.sleep(0.1)
        return 'REPEAT'
#############################################################################################################################################################

class DEINITIALISE(smach.State):
    global status_handler
    global _namespace
    #global scMsg

    def __init__(self):
        smach.State.__init__(self, outcomes=['SUCCESS', 'REPEAT','FAIL'])
        self.rate = rospy.Rate(1)
        self.stateMsg = StateMsg()



    def execute(self, userdata):
        rospy.loginfo(_namespace + 'On DEINITIALISE state')
        #rospy.Subscriber('/stage_counter_topic', String, self.deinitialise_callback)
        #status_handler.publishRoverSC(self.scMsg)
        #self.scMsg += 1
        status_handler.sc += 1
        status_handler.publishRoverSC(status_handler.sc)
        print("stage:", status_handler.sc)
        status_handler.deinitialise()
        rospy.sleep(1)
        return 'SUCCESS'

    def deinitialise_callback(self,data):
        self.x = data.data





class ERROR(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['KILL', 'REPEAT','NOT_BAD'])

    def execute(self, userdata):
        rospy.loginfo('On ERROR state')
        rospy.sleep(0.1)
        return 'NOT_BAD'


#####################################################################################################################################################


def CreateStateMachine():

    #Create the state machine
    sm_rover = smach.StateMachine(outcomes=['DEAD'])

    #Open the container
    with sm_rover:

        smach.StateMachine.add('INITIALISE', INITIALISE(),
                               transitions={'SUCCESS': 'READY', 'REPEAT': 'INITIALISE', 'FAIL': 'ERROR'})

        smach.StateMachine.add('READY', READY(),
                               transitions={'TO_GPS': 'REACH_GPS', 'FAIL': 'ERROR', 'REPEAT':'READY'})

        smach.StateMachine.add('REACH_GPS', REACH_GPS(),
                               transitions={'SUCCESS': 'FIND_ARTAG', 'SUCCES12': 'DEINITIALISE','IMAGE_INTERRUPT' : 'REACH_ARTAG','FAIL': 'ERROR', 'REPEAT': 'REACH_GPS'})

        smach.StateMachine.add('FIND_ARTAG',FIND_ARTAG(),
                               transitions={'SUCCESS': 'REACH_ARTAG', 'GO_APPROACH':'APPROACH' , 'FAIL': 'ERROR', 'REPEAT': 'FIND_ARTAG'})

        smach.StateMachine.add('APPROACH', APPROACH(),
                               transitions={'SUCCESS': 'PASS_GATE', 'FAIL': 'ERROR', 'REPEAT': 'APPROACH'})

        smach.StateMachine.add('PASS_GATE', PASS_GATE(),
                               transitions={'SUCCESS': 'DEINITIALISE', 'FAIL': 'ERROR', 'REPEAT_APPROACH' : 'APPROACH'})

        smach.StateMachine.add('REACH_ARTAG', REACH_ARTAG(),
                               transitions={'SUCCESS': 'DEINITIALISE', 'FAIL': 'ERROR', 'REPEAT': 'REACH_ARTAG','BACK':'FIND_ARTAG'})

        smach.StateMachine.add('DEINITIALISE', DEINITIALISE(),
                               transitions={'SUCCESS': 'INITIALISE', 'FAIL': 'ERROR', 'REPEAT': 'DEINITIALISE'})

        smach.StateMachine.add('ERROR', ERROR(),
                               transitions={'KILL': 'DEAD', 'REPEAT': 'ERROR','NOT_BAD':'DEINITIALISE'})



    #Codes for smach viewer
    sis = smach_ros.IntrospectionServer('rover20_state_machine', sm_rover, '/ROVER_SM_ROOT')
    sis.start()

    outcome = sm_rover.execute()
    sis.stop()


def main():
    #Init,pubs and subs
    rospy.init_node("state_machine")
    global _namespace
    global status_handler

    #scMsg = status_handler.sc
    status_handler.start()
    #scMsg = status_handler.sc

    while not rospy.is_shutdown():
        CreateStateMachine()
        rospy.loginfo(_namespace + "Created State Machine..")



if __name__ == '__main__':
    main()
    rospy.spin()
