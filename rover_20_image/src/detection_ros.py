#!/usr/bin/env python

import cv2
import numpy as np
import rospy
from std_msgs.msg import String
#from timeit import default_timer as timer


class tags:
    valids = {
        "1":np.array([
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1],
        ], dtype=int),

        "2":np.array([
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [0, 0, 1, 1, 0],
            [1, 1, 1, 0, 1],
        ], dtype=int),

        "3":np.array([
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 0, 1, 1, 0],
            [1, 0, 1, 1, 0],
        ], dtype=int),

        "4": {
            "l":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [0, 1, 1, 1, 1],
                [1, 0, 1, 0, 0],
            ], dtype=int),

            "r":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ], dtype=int),
        },

        "5": {
            "l":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 1, 1],
                [0, 1, 1, 0, 0],
            ], dtype=int),
            "r":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [0, 0, 1, 1, 1],
                [0, 0, 1, 1, 1],
            ], dtype=int),
        },

        "6":{
            "l":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
                [0, 0, 1, 0, 1],
            ], dtype=int),

            "r":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [0, 0, 1, 0, 1],
                [1, 1, 1, 1, 0],
            ], dtype=int),
        },

        "7":{
            "l":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 1, 1, 0, 0],
                [1, 1, 1, 0, 0],
            ], dtype=int),

            "r":np.array([
                [1, 1, 0, 1, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [0, 1, 1, 0, 0],
                [1, 0, 1, 1, 1],
            ], dtype=int),
        }
    }


class params:
    threshConstant = 7
    threshWinSizeMax = 23
    threshWinSizeMin = 3
    threshWinSizeStep = 10
    accuracyRate = 0.02
    minAreaRate = 0.03
    maxAreaRate = 6
    minCornerDisRate = 1.5
    minMarkerDisRate = 1
    resizeRate = 8
    cellMarginRate = 0.13
    markerSizeInBits = 5
    borderSizeInBits = 2
    configFileName = 'logi-g922-config.json'
    undistortImg = False
    showCandidate = True
    showMarkers = True
    showTresholded = True
    correctedBits = 3


def load_camera_params(filename='default.json'):
    with open(filename, 'r') as loadFile:
        data = json.load(loadFile)
        mtx = np.array(data['mtx'])
        dist = np.array(data['dist'])
    return mtx, dist


def remove_close_candidates(candidates):
    newCandidates = list()

    for i in range(len(candidates)):
        for j in range(len(candidates)):
            if i == j:
                continue

            minPerimeter = min(cv2.arcLength(candidates[i], True), cv2.arcLength(candidates[j], True))

            for fc in range(4):
                disSq = 0
                for c in range(4):
                    modC = (fc + c) % 4
                    dx = candidates[j][c][0][0] - candidates[i][modC][0][0]
                    dy = candidates[j][c][0][1] - candidates[i][modC][0][1]
                    disSq += dx * dx + dy * dy
                disSq /= 4

                minDisPixels = minPerimeter * params.minMarkerDisRate

                if disSq < minDisPixels * minDisPixels:
                    if cv2.contourArea(candidates[i]) > cv2.contourArea(candidates[j]):
                        newCandidates.append(candidates[i])
                    else:
                        newCandidates.append(candidates[j])

    if len(newCandidates):
        return newCandidates
    else:
        return candidates


def has_close_corners(candidate):
    minDisSq = float("inf")

    for i in range(len(candidate)):
        dx = candidate[i][0][0] - candidate[(i+1)%4][0][0]
        dy = candidate[i][0][1] - candidate[(i+1)%4][0][1]
        dsq = dx * dx + dy * dy
        minDisSq = min(minDisSq, dsq)

    minDisPixel = candidate.size * params.minCornerDisRate
    if minDisSq < minDisPixel * minDisPixel:
        return True
    else:
        return False


def sort_corners(corners):
   dx1 = corners[1][0] - corners[0][0]
   dy1 = corners[1][1] - corners[0][1]
   dx2 = corners[2][0] - corners[0][0]
   dy2 = corners[2][1] - corners[0][1]

   crossproduct = (dx1 * dy2) - (dy1 * dx2)

   if crossproduct > 0:
       corners[1], corners[3] = corners[3], corners[1]


def get_corners(candidate):
    corners = np.array([
        [candidate[0][0][0], candidate[0][0][1]],
        [candidate[1][0][0], candidate[1][0][1]],
        [candidate[2][0][0], candidate[2][0][1]],
        [candidate[3][0][0], candidate[3][0][1]]
    ], dtype="float32")
    return corners


def get_candate_img(candidate, frame):
    corners = get_corners(candidate)
    sort_corners(corners)

    (tl, tr, br, bl) = corners
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))#

    dst = np.array(
        [[0, 0],
         [maxWidth - 1, 0],
         [maxWidth-1, maxHeight-1],
         [0, maxHeight - 1]
         ], dtype="float32"
    )

    M = cv2.getPerspectiveTransform(corners, dst)
    warped = cv2.warpPerspective(frame, M, (maxWidth, maxHeight), borderMode=cv2.INTER_NEAREST)

    return warped


def validate_candidates(candidates, frame):
    markers = list()
    bestCan = None       # LEFT
    bestCan1 = None      # RIGHT
    lowestError = params.markerSizeInBits * params.markerSizeInBits
    lowestError1 = params.markerSizeInBits * params.markerSizeInBits

    validMarker = tags.valids[stage]

    for can in candidates:
        candidate_img = get_candate_img(can, frame)
        candidate_img = resize_img(candidate_img)

        #cv2.imshow("wdew", candidate_img)
        ret, candidate_img = cv2.threshold(candidate_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #cv2.imshow("wdeaw", candidate_img)

        bits = extract_bits(candidate_img)
        bits = np.transpose(bits)

        #rospy.Subscriber('/stage', String, stage_callback)

        if int(stage) <= 3:
            validMarker = tags.valids["4"]["r"]     #TODO: i made changes for test purposes. must fix before final relaese
            wrongBits = np.count_nonzero(np.subtract(bits,validMarker))
            if  wrongBits <= params.correctedBits and wrongBits < lowestError:
                bestCan = can
                lowestError = wrongBits
        else:
            validMarkerLeft = tags.valids[stage]["l"]
            validMarkerRight = tags.valids[stage]["r"]

            wrongBits = np.count_nonzero(np.subtract(bits,validMarkerLeft))
            wrongBits1 = np.count_nonzero(np.subtract(bits,validMarkerRight))

            if wrongBits < lowestError and wrongBits <= params.correctedBits:
                bestCan = can
            if wrongBits1 < lowestError1 and wrongBits1 <= params.correctedBits:
                bestCan1 = can

    if bestCan is not None:
        markers.append(bestCan)
    if bestCan1 is not None:
        markers.append(bestCan)

    return markers


def recreate_img(bits):
    cellSize = 30
    img = np.zeros((bits.shape[0] * cellSize, bits.shape[1] * cellSize, 1))

    for j in range(bits.shape[0]):
        for i in range(bits.shape[1]):
            if bits[j, i] == 0:
                continue
            for x in range(cellSize):
                ix = i * cellSize + x
                for y in range(cellSize):
                    iy = j * cellSize + y
                    img[iy, ix] = 255

    return img


def resize_img(inputImg):
    w = int(inputImg.shape[1]*params.resizeRate)
    h = int(inputImg.shape[0]*params.resizeRate)
    outputImg = cv2.resize(inputImg, (w,h))
    return outputImg


def extract_bits(img):
    markerSize = params.markerSizeInBits
    borderSize = params.borderSizeInBits

    markerSizeWithBorders = markerSize + 2 * borderSize
    bitmap = np.zeros((markerSize, markerSize), dtype=int)
    cellWidth = int(img.shape[1] / markerSizeWithBorders)
    cellHeight = int(img.shape[0] / markerSizeWithBorders)

    inner_rg = img[borderSize*cellHeight:(markerSizeWithBorders-borderSize)*cellHeight,
               borderSize*cellWidth:(markerSizeWithBorders-borderSize)*cellWidth]

    marginX = int(cellWidth * params.cellMarginRate)
    marginY = int(cellHeight * params.cellMarginRate)

    for j in range(markerSize):
        Ystart = j * cellHeight
        for i in range(markerSize):
            Xstart = i * cellWidth
            bitImg = inner_rg[Ystart+marginY:Ystart+cellHeight-marginY, Xstart+marginX:Xstart+cellWidth-marginX]
            if np.count_nonzero(bitImg) / bitImg.size > 0.5:
                bitmap[j][i] = 1

    return bitmap


def detect_candidates(grayImg):
    th = cv2.adaptiveThreshold(grayImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 9, params.threshConstant)
    cnts = cv2.findContours(th, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[-2]

    if params.showTresholded is True:
        cv2.imshow('treshold', th)

    candidates = list()
    for c in cnts:
        maxSize = int(max(gray.shape) * params.maxAreaRate)
        minSize = int(max(gray.shape) * params.minAreaRate)
        if c.size > maxSize or c.size < minSize:
            continue

        approxCurve = cv2.approxPolyDP(c, len(c) * params.accuracyRate, True)
        if len(approxCurve) is not 4 or cv2.isContourConvex(approxCurve) is False:
            continue

        if has_close_corners(approxCurve):
            continue

        candidates.append(approxCurve)

    return candidates


def find_center(marker):
    (x, y), r = cv2.minEnclosingCircle(marker)
    return int(x), int(y), int(r)


def stage_callback(msg):
    stage = msg.data



rospy.init_node('rover_detect_artag')
coordinatePublisher = rospy.Publisher("/px_coordinates", String, queue_size = 1)
coordinatePublisher1 = rospy.Publisher("/px_coordinates1", String, queue_size = 1)
sidePublisher = rospy.Publisher("/is_behind", String, queue_size = 1)

stage = "1"
camera = cv2.VideoCapture(1)
mtx = None
dist = None

if params.undistortImg is True:
    mtx, dist = load_camera_params(filename=params.configFileName)

while not rospy.is_shutdown():
    _, frame = camera.read()

    if params.undistortImg is True:
        frame = cv2.undistort(frame, mtx, dist)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    candidates = detect_candidates(gray)

    # this piece of code is messy a bit
    # TODO: optimize it
    if len(candidates) > 0:
        markers = validate_candidates(candidates, gray)

        if params.showCandidate is True:
            cv2.drawContours(frame, candidates, -1, (0, 255, 0), 2)

        if len(markers) > 0 and params.showMarkers is True:
            cv2.drawContours(frame, markers, -1, (255, 0, 0), 3)
        else:
            coordinatePublisher.publish("-")
            coordinatePublisher1.publish("-")
            sidePublisher.publish("-")

        if len(markers) > 2:
            w = frame.shape[1]
            h = frame.shape[0]
            x,y,r = find_center(markers[0])
            coordinatePublisher.publish(str(x) +","+ str(y) + "," + str(w) + "," + str(h)+ "," + str(r))
            x1,y,r = find_center(markers[1])
            coordinatePublisher1.publish(str(x1) +","+ str(y) + "," + str(w) + "," + str(h)+ "," + str(r))

            if x1 < x:
                sidePublisher.publish("1")
            else:
                sidePublisher.publish("0")
    else:
        coordinatePublisher.publish("-")
        coordinatePublisher1.publish("-")
        sidePublisher.publish("-")

    cv2.imshow('frame', frame)
    if cv2.waitKey(10) == 27:
        break
