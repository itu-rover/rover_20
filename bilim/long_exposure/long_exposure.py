# import the necessary packages
import argparse
import imutils
import cv2
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True,
	help="path to input video file")
ap.add_argument("-o", "--output", required=True,
	help="path to output 'long exposure'")
args = vars(ap.parse_args())

# initialize the Red, Green, and Blue channel averages, along with
# the total number of frames read from the file

(rAvg, gAvg, bAvg) = (None, None, None)
total = 0


# open a pointer to the video file
print("[INFO] opening video file pointer...")
stream = cv2.VideoCapture(args["video"])   
print("[INFO] computing frame averages (this will take awhile)...")


# loop over frames from the video file stream
while True:
	# grab the frame from the file stream
	(grabbed, frame) = stream.read()
 
	# if the frame was not grabbed, then we have reached the end of
	# the sfile
	if not grabbed:
		break
 
	# otherwise, split the frmae into its respective channels
	(B, G, R) = cv2.split(frame.astype("float"))

	# if the frame averages are None, initialize them
	if rAvg is None:
		rAvg = R
		bAvg = B
		gAvg = G

	# otherwise, compute the weighted average between the history of
	# frames and the current frames
	else:
		rAvg = ((total * rAvg) + (1 * R)) / (total + 1.0)
		gAvg = ((total * gAvg) + (1 * G)) / (total + 1.0)
		bAvg = ((total * bAvg) + (1 * B)) / (total + 1.0)
 
	# increment the total number of frames read thus far
	total += 1
 

# merge the RGB averages together and write the output image to disk
avg = cv2.merge([bAvg, gAvg, rAvg]).astype("uint8")
cv2.imwrite(args["output"], avg)

# do a bit of cleanup on the file pointer
stream.release()


