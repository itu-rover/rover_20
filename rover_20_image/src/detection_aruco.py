#!/usr/bin/env python

import cv2
import numpy as np
import rospy
import cv2.aruco as aruco
import json
from std_msgs.msg import String


def get_dictionary():
    aruco_dict = aruco.custom_dictionary(0, 5, 1)
    aruco_dict.bytesList = np.empty(shape=(11, 4, 4), dtype=np.uint8)

    # LEG 1
    mybits = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 1],
        [0, 0, 1, 0, 1]
    ], dtype=np.uint8)
    aruco_dict.bytesList[0] = aruco.Dictionary_getByteListFromBits(mybits)

    # LEG 2
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 1, 0],
        [1, 1, 1, 0, 1]
    ], dtype=np.uint8)
    aruco_dict.bytesList[1] = aruco.Dictionary_getByteListFromBits(mybits)

    # LEG 3
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 1, 0],
        [1, 0, 1, 1, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[2] = aruco.Dictionary_getByteListFromBits(mybits)

    # LEG 4
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1],
        [1, 0, 1, 0, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[3] = aruco.Dictionary_getByteListFromBits(mybits)
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [0, 1, 1, 1, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[4] = aruco.Dictionary_getByteListFromBits(mybits)

    # LEG 5
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 1, 1, 1],
        [0, 1, 1, 0, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[5] = aruco.Dictionary_getByteListFromBits(mybits)
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 1, 1],
        [0, 0, 1, 1, 1]
    ], dtype=np.uint8)
    aruco_dict.bytesList[6] = aruco.Dictionary_getByteListFromBits(mybits)

    # LEG 6
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 1, 0],
        [0, 0, 1, 0, 1]
    ], dtype=np.uint8)
    aruco_dict.bytesList[7] = aruco.Dictionary_getByteListFromBits(mybits)
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1],
        [1, 1, 1, 1, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[8] = aruco.Dictionary_getByteListFromBits(mybits)

    #  LEG 7
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 0, 0]
    ], dtype=np.uint8)
    aruco_dict.bytesList[9] = aruco.Dictionary_getByteListFromBits(mybits)
    mybits = np.array([
        [1, 1, 0, 1, 1],
        [1, 1, 0, 1, 1],
        [1, 0, 1, 0, 1],
        [0, 1, 1, 0, 0],
        [1, 0, 1, 1, 1]
    ], dtype=np.uint8)
    aruco_dict.bytesList[10] = aruco.Dictionary_getByteListFromBits(mybits)

    return aruco_dict

def find_center(marker):
    (x, y), r = cv2.minEnclosingCircle(marker)
    return int(x), int(y), int(r)

def load_camera_params(filename='/home/berkealgul/rover_20_ws/src/rover_20/rover_20_image/src/logi-g922-config.json'):
    with open(filename, 'r') as loadFile:
        data = json.load(loadFile)
        mtx = np.array(data['mtx'])
        dist = np.array(data['dist'])
    return mtx, dist

def stage_callback(data):
    global stage, leftId , rightId
    stage = int(data.data)
    
    if stage < 4:
        leftId = stage  # We got single artagr rather than a gate we still use leftId as our artag
        rightId = -1    # Since there is no gate in bellow stage 3, right id is not valid
    else:
        leftId = (stage - 4) * 2 + 3    # when there is a gate we use this formula to find our ids
        rightId = leftId + 1


def main(mtx, dist):
    cap = cv2.VideoCapture(0)

    # ID 1 had changed for test purposes. TODO:Must fix before URC
    aruco_dict = get_dictionary()
    parameters = aruco.DetectorParameters_create()
    parameters.markerBorderBits = 2  

    while not rospy.is_shutdown():
        rospy.Subscribe('/stage_counter_topic', String, stage_callback)
        
        print("L: " + str(leftId) + " R: " + print(rightId))

        ret, frame = cap.read()

        corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict,
                                                                parameters=parameters,
                                                                cameraMatrix=mtx,
                                                                distCoeff=dist)

        if np.all(ids is not None):  # If there are markers found by detector
            for i in range(0, len(ids)):
                print(ids[i])
                # Estimate pose of each marker and return the values rvec and tvec---different from camera coefficients
                rvec, tvec, markerPoints = aruco.estimatePoseSingleMarkers(corners[i], 0.02, mtx, dist)
                (rvec - tvec).any()  # get rid of that nasty numpy value array error
                aruco.drawAxis(frame, mtx, dist, rvec, tvec, 0.01)  
            aruco.drawDetectedMarkers(frame, corners)

        if len(ids) == 2:
            w = frame.shape[1]
            h = frame.shape[0]
            x,y,r = find_center(corners[0])
            coordinatePublisher.publish(str(x) +","+ str(y) + "," + str(w) + "," + str(h)+ "," + str(r))
            
            x,y,r = find_center(corners[1])
            coordinatePublisher1.publish(str(x) +","+ str(y) + "," + str(w) + "," + str(h) +"," + str(r))
         elif len(ids) == 1:
            w = frame.shape[1]
            h = frame.shape[0]
            x,y,r = find_center(corners[0])
            coordinatePublisher.publish(str(x) +","+ str(y) + "," + str(w) + "," + str(h) + "," + str(r))
         else:
            coordinatePublisher.Publish('-')
            coordinatePublisher1.Publish('-')

        cv2.imshow('frame', frame)
        dir_pub.Publish("1")

        key = cv2.waitKey(3) & 0xFF
        if key == ord('q'):  # Quit
            break

    cap.release()
    cv2.destroyAllWindows()


rospy.init_node('rover_detect_artag')

stage = "1"
leftId = 0
rightId = 0

mtx, dis = load_camera_params()
coordinatePublisher = rospy.Publisher('/px_coordinates', String, queue_size = 1)
coordinatePublisher1 = rospy.Publisher('/px_coordinates1', String, queue_size = 1)
dir_pub = rospy.Publisher('/artag_direction', String, queue_size = 1)


main(mtx, dist)
