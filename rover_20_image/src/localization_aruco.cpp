#include <iostream>
#include <vector>
#include <ros/ros.h>
#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>

using namespace cv;
using namespace aruco;


int main(int argc, char **argv)
{
	ros::init(argc, argv, "localization_aruco");

	Mat_<double> mtx(3,3);
	Mat_<double> dist(1,5);
	Mat frame;

	std::vector<std::vector<Point2f>> corners;
	std::vector<int> ids;
	std::vector<Vec3d> rvecs, tvecs;
	Ptr<DetectorParameters> params = DetectorParameters::create();
	Ptr<Dictionary> dictionary = getPredefinedDictionary(DICT_5X5_250);

	VideoCapture cap;
	
	dist << 0.020436355102596344, -0.11407839179793304, 0.004229887050454093, -0.01709654130034178, 0.13991605472148272;
    mtx << 627.2839475395182, 0.0, 295.0153571445745,
           0.0, 630.6046803340988, 237.10098847214766,
           0.0, 0.0, 1.0;

	cap.open(0);

	if(!cap.isOpened())
	{
		std::cout << "-------------------------------------------\n\n";
		std::cout << "   Camera is not open! Shutting down!\n\n";
		std::cout << "-------------------------------------------";
		return 1;
	}

	while(ros::ok())
	{
		cap.read(frame);

		detectMarkers(frame, dictionary, corners, ids ,params);
		estimatePoseSingleMarkers(corners, 0.2, mtx, dist, rvecs, tvecs);

		if(ids.size() > 0)
		{
			drawDetectedMarkers(frame, corners);

			for (int i = 0, n = tvecs.size(); i < n; ++i)
			{
				drawAxis(frame, mtx, dist, rvecs[i], tvecs[i], 1);
			}
		}

		imshow("frame", frame);

		ros::spinOnce();
		if(waitKey(10) == 27) //27 == esc
			break;
	}

	return 0;
}
