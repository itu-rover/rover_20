#include <iostream>
#include "ar_tracker.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "aruco_slam");

	VideoCapture cap;
	cap.open(1);

	if(!cap.isOpened())
	{
		std::cout << "-------------------------------------------\n\n";
		std::cout << "   Camera is not open! Shutting down!\n\n";
		std::cout << "-------------------------------------------";
		return 1;
	}
	else
		std::cout << "---------------Camera Opended!!!--------------\n";


	Mat_<double> mtx(3,3);
	Mat_<double> dist(1,5);
	dist << 0.020436355102596344, -0.11407839179793304, 0.004229887050454093, -0.01709654130034178, 0.13991605472148272;
	mtx << 627.2839475395182, 0.0, 295.0153571445745,
		   0.0, 630.6046803340988, 237.10098847214766,
		   0.0, 0.0, 1.0;

	ArTracker::parameters *params = ArTracker::create_parameters();
	ArTracker::run(cap, mtx, dist, params);

	return 0;
}