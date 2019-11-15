#!/usr/bin/env python
#This is the bearing calculator code for ITU ROVER TEAM
import rospy
from std_msgs.msg import String
import rosparam


pxCoordinateTopic = rospy.get_param('RoverReachImage/CalculateBearing/sub_pxCoordinates','/px_coordinates')
bearingPub = rospy.get_param('RoverReachImage/CalculateBearing/pub_bearing','/bearing_to_ball')
camAngleOfView = rospy.get_param('RoverReachImage/CalculateBearing/camAngleOfView', 110)

pxCoordinates = [None]*2
videoWidth = None
videoHeight = None
calculatedBearing = None
noBall = True

def pxCallback(data):
    global pxCoordinates
    global videoHeight
    global videoWidth
    global noBall
    if(data.data != '-'):
        pxCoordinates[0] = float(data.data.split(',')[0])
        pxCoordinates[1] = float(data.data.split(',')[1])
        videoWidth = float(data.data.split(',')[2])
        videoHeight = float(data.data.split(',')[3])
        noBall = False
    else:
        noBall = True
    
    
def calculateBearing(pxWidth, pxHeight, videoWidth, videoHeight):
    global calculatedBearing
    global noBall
    if pxWidth != None and videoWidth != None and noBall == False :
        center = videoWidth / 2
        anglePerPixel = camAngleOfView/videoWidth
        diff = center - pxWidth
        if diff > 5:
            print("+" + str(abs(diff*anglePerPixel)))            
            calculatedBearing = "+"+str(abs(diff * anglePerPixel))
        elif diff < -5:
            print("-" + str(abs(diff*anglePerPixel)))
            calculatedBearing = "-"+str(abs(diff * anglePerPixel))
        else:
            print("Duz")
            calculatedBearing= "0"
        
    else:
        calculatedBearing = "-"

    rospy.sleep(0.04)
        


def printIt(pxWidth,pxHeight,videoWidth,videoHeight):    
    print("pxWidth : "+ str(pxWidth) + " pxHeight : " + str(pxHeight) + " videoWidth : " + str(videoWidth) + " videoHeight : " + str(videoHeight))
    

def main():
    global pxCoordinates
    global videoWidth
    global videoHeight
    global calculatedBearing
    while not rospy.is_shutdown():
        calculateBearing(pxCoordinates[0],pxCoordinates[1],videoWidth,videoHeight)
        if(calculatedBearing != None):
            bearingPublisher.publish(calculatedBearing)

    rospy.spin()

if __name__ == '__main__':

    try:
        rospy.init_node('bearing')       
        bearingPublisher = rospy.Publisher(bearingPub,String,queue_size = 100)
        rospy.Subscriber(pxCoordinateTopic, String, pxCallback)
        while not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass





        





    


















