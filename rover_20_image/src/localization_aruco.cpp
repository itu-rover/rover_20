#include <iostream>
#include <vector>
#include <ros/ros.h>
#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>

using namespace cv;
using namespace aruco;


int main(int argc, char **argv)
{
	ros::init(argc, argv, "aruco_cpp");

	Mat frame;
	std::vector<std::vector<Point2f>> corners;
	std::vector<int> ids;
	VideoCapture cap;
	Ptr<DetectorParameters> params = DetectorParameters::create();
	Ptr<Dictionary> dictionary = getPredefinedDictionary(DICT_5X5_250);
	params->markerBorderBits = 2;

	cap.open(0);

	if(!cap.isOpened())
	{
		std::cout << "Camera is not open! Shutting down!\n";
		return 1;
	}

	while(ros::ok())
	{
		cap.read(frame);

		detectMarkers(frame, dictionary, corners, ids ,params);

		if(ids.size() > 0)
			drawDetectedMarkers(frame, corners);
		//std::cout << ids << '\n';
		imshow("frame", frame);

		ros::spinOnce();
		if(waitKey(10) == 27) //27 == esc
			break;
	}

	return 0;
}
