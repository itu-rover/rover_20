import numpy as np
import os
import cv2
import time


filename = 'bilim_15_seconds.avi'
frames_per_second = 10.0
res = '480p'     #480p yaplabilir


def resolution(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)


STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    resolution(cap, width, height)
    return width, height

VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}

def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']



cap = cv2.VideoCapture(0)
out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cap, res))

i=0
second=440
while i in range (second):
    ret, frame = cap.read()
    out.write(frame)
    cv2.imshow('frame',frame)
    i +=1
    if second-i ==0:
    	break
    cv2.waitKey(1)   
    time.sleep(0.002)

cap.release()
out.release()
cv2.destroyAllWindows()