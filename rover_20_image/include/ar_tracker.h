#include <iostream>
#include <string>
#include <vector>
#include <tuple>
#include <opencv2/opencv.hpp>
#include <opencv2/aruco.hpp>
#include <ros/ros.h>
#include <tf/LinearMath/Matrix3x3.h>
#include <tf/transform_broadcaster.h>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.h>
#include "definitions.h"

#define PI 3.14159265358979323846
#define FIXED_FRAME "aruco_slam_world"

using namespace cv;
using namespace aruco;

class ArTracker
{
public:

	//aruco stoff
	Ptr<DetectorParameters> params;
	Ptr<Dictionary> dictionary;

	//opencv stuff
	VideoCapture cap;
	Mat_<double> mtx(3,3);
	Mat_<double> dist(1,5);
	dist << 0.020436355102596344, -0.11407839179793304, 0.004229887050454093, -0.01709654130034178, 0.13991605472148272;
	mtx << 627.2839475395182, 0.0, 295.0153571445745,
		   0.0, 630.6046803340988, 237.10098847214766,
		   0.0, 0.0, 1.0;

	//ros stuff
	ros::NodeHandle n;
	tf::TransformBroadcaster br;

	//tree stuff
	slam_tree tree;

	//custom stuff
	int iter;
	bool showFrame;

	//functions
	ArTracker();

	void step();
	void relocalize_marker(slam_obj* marker, slam_obj* camera, tf::Quaternion R_cm, tf::Vector3 T_cm);
	void broadcast_tf(tf::TransformBroadcaster br, slam_obj *obj);
	void update_camera_transform(slam_obj* camera, std::vector<tf::Quaternion> qv, std::vector<tf::Vector3> tv);

	std::tuple<tf::Quaternion, tf::Vector3> estimate_cam_transform(tf::Quaternion R_cm, tf::Vector3 T_cm ,slam_obj *camera, slam_obj *marker);
	slam_obj *create_marker_obj(tf::Quaternion R_cm, tf::Vector3 T_cm, int id, slam_obj* camera);
	slam_obj *create_camera();	
};

ArTracker::ArTracker()
{
	dictionary = getPredefinedDictionary(DICT_5X5_250);
	params = DetectorParameters::create();
	tree.add(create_camera());
	iter = 0;
	showFrame = true;
}


void ArTracker::step()
{
	Mat frame;
	std::vector<std::vector<Point2f>> corners;
	std::vector<int> ids;
	std::vector<Vec3d> rvecs, tvecs;

	cap.read(frame);

	cv::aruco::detectMarkers(frame, dictionary, corners, ids ,params);

	if(ids.size() > 0)
	{
		slam_obj *cam = tree.search_id(-1);

		estimatePoseSingleMarkers(corners, 0.2, mtx, dist, rvecs, tvecs);
		drawDetectedMarkers(frame, corners);

		std::vector<tf::Quaternion> cam_orientations;
		std::vector<tf::Vector3>    cam_locations;

		for (int i = 0, n = ids.size(); i < n; i++)
		{
			int id = ids[i];
			Vec3d r = rvecs[i];
			Vec3d t = tvecs[i];

			drawAxis(frame, mtx, dist, r, t, 0.1);

			tf::Vector3 T_cm;
			tf::Quaternion R_cm;
			T_cm = tf::Vector3(t[0],t[1],t[2]);
			R_cm.setRPY(r[0], r[1], r[2]);

			slam_obj *marker = tree.search_id(id);

			// If marker is not exist in map(slam system) we will add it
			// otherwise estimate cam transform with it 
			// Note: Markers are assumed to be static
			if(marker == NULL)
			{
				marker = create_marker_obj(R_cm, T_cm, id, cam);
				tree.add(marker);
			}
			else
			{
				tf::Quaternion R;
				tf::Vector3 T;

				std::tie(R, T) = estimate_cam_transform(R_cm, T_cm, cam, marker);

				cam_orientations.push_back(R);
				cam_locations.push_back(T);
			}
		}

		//Update camera 
		if(iter % 3 == 0)
			update_camera_transform(cam, cam_orientations, cam_locations);
	}

	tree.traverse(br, broadcast_tf);
	iter++;
	if(showFrame)
		imshow("frame", frame);
	waitKey(1);
}


void ArTracker::relocalize_marker(slam_obj* marker, slam_obj* camera, tf::Quaternion R_cm, tf::Vector3 T_cm)
{
	tf::Quaternion R_wc = camera->R;
	tf::Quaternion R_wm = R_wc * R_cm;

	tf::Vector3 T_wc = camera->T;
	tf::Vector3 T_wm = T_wc + (tf::Matrix3x3(R_wc) * T_cm);

	marker->T = T_wm;
	marker->R = R_wm;
}

slam_obj* ArTracker::create_marker_obj(tf::Quaternion R_cm, tf::Vector3 T_cm, int id, slam_obj* camera)
{
	tf::Quaternion R_wc = camera->R;
	tf::Quaternion R_wm = R_wc * R_cm;

	tf::Vector3 T_wc = camera->T;
	tf::Vector3 T_wm = T_wc + (tf::Matrix3x3(R_wc) * T_cm);

	slam_obj *marker = new slam_obj;

	marker->id = id;
	//marker->relocalization_cooldown_counter = RELOCALIZATION_COOLDOWN;
	marker->name = "id="+std::to_string(id);
	marker->R = R_wm;
	marker->T = T_wm;
	marker->left = NULL;
	marker->right = NULL;

	return marker;
}

std::tuple<tf::Quaternion, tf::Vector3>  ArTracker::estimate_cam_transform(tf::Quaternion R_cm, tf::Vector3 T_cm ,slam_obj *camera, slam_obj *marker)
{
	tf::Vector3 T_wm = marker->T, T_wc = camera->T;
	tf::Quaternion R_wm = marker->R, R_wc = camera->R;

	T_wc = T_wm - (tf::Matrix3x3(R_wc) * T_cm);
	R_wc = R_wm * R_cm.inverse();

	return std::make_tuple(R_wc, T_wc);
}

slam_obj* ArTracker::create_camera()
{
	slam_obj *camera = new slam_obj;
	//we assumed that all markers have positive id.
	//hence with -1 id, camera can be in tree while 
	//can be distinguished from markers
	camera->id = -1;
	camera->name = "c922";
	//the initial rotation and position of the camera can be changed 
	//but not recommended
	camera->R.setRPY(PI/2, PI, 0);
	camera->T = tf::Vector3(0, 0, 0);
	camera->left = NULL;
	camera->right = NULL;
	
	return camera;
}

void ArTracker::broadcast_tf(tf::TransformBroadcaster br, slam_obj *obj)
{
	tf::Transform transform;
	transform.setOrigin(obj->T);
	transform.setRotation(obj->R);
	br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), FIXED_FRAME, obj->name));
}

void ArTracker::update_camera_transform(slam_obj* camera, std::vector<tf::Quaternion> qv, std::vector<tf::Vector3> tv)
{	
	tf::Quaternion R = camera->R;
	tf::Vector3 T = camera->T;

	int n = qv.size();

	if(n == 0)
		return;

	else if(n == 1)
	{
		camera->R = qv[0];
		camera->T = tv[0];
		return;
	}

	float confidenseTreshold = 0.1f;
	float minDot = R.dot(qv[0]);
	float minDis = T.distance(tv[0]);

	tf::Quaternion qMin = qv[0];
	tf::Vector3 tMin = tv[0];

	for(auto q : qv)
	{
		float dot = R.dot(q);

		if(dot < minDot)
		{
			minDot = dot;
			qMin = q;
		}
	}

	for(auto t : tv)
	{
		float dis = T.distance(t);

		if(dis < minDis)
		{
			minDis = dis;
			tMin = t;
		}
	}

	float dot = qMin.dot(camera->R);
	float dis = tMin.distance(camera->T);

	if(dot < confidenseTreshold && dis < confidenseTreshold) 
	{
		camera->R = qMin;
		camera->T = tMin;
	}
}
