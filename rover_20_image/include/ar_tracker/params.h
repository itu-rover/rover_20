#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>

using namespace cv;
using namespace aruco;

namespace ArTracker
{

struct parameters
{
	int update_cam_interval;
	float transform_confidence_tresh; 
	Ptr<DetectorParameters> aruco_params;
	Ptr<Dictionary> dictionary;
};

//default params are defined here
parameters *create_parameters()
{
	parameters *p = new parameters;

	p->update_cam_interval = 3;
	p->transform_confidence_tresh = 0.3;
	p->aruco_params = DetectorParameters::create();
	p->dictionary = getPredefinedDictionary(DICT_5X5_250);

	return p;
}  	

}