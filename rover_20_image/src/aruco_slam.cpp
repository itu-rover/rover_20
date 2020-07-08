#include <iostream>
#include <string>
#include <vector>
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

void broadcast_tf(tf::TransformBroadcaster br, slam_obj *obj);
slam_obj *create_camera();
void update_cam_transform(tf::Quaternion R_cm, tf::Vector3 T_cm ,slam_obj *camera, slam_obj *marker);
slam_obj *create_marker_obj(tf::Quaternion R_cm, tf::Vector3 T_cm, int id, slam_obj* camera);


int main(int argc, char **argv)
{
	ros::init(argc, argv, "aruco_slam");

	//aruco stoff
	std::vector<std::vector<Point2f>> corners;
	std::vector<int> ids;
	std::vector<Vec3d> rvecs, tvecs;
	Ptr<DetectorParameters> params = DetectorParameters::create();
	Ptr<Dictionary> dictionary = getPredefinedDictionary(DICT_5X5_250);

	//opencv stuff
	VideoCapture cap;
	Mat frame;
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
	tree.add(create_camera());

	cap.open(0);

	if(!cap.isOpened())
	{
		std::cout << "-------------------------------------------\n\n";
		std::cout << "   Camera is not open! Shutting down!\n\n";
		std::cout << "-------------------------------------------";
		return 1;
	}
	else
		std::cout << "---------------Camera Opended!!!--------------\n";


	while(ros::ok())
	{
		cap.read(frame);

		detectMarkers(frame, dictionary, corners, ids ,params);
		estimatePoseSingleMarkers(corners, 0.2, mtx, dist, rvecs, tvecs);

		if(ids.size() > 0)
		{
			slam_obj *cam = tree.search_id(-1);

			drawDetectedMarkers(frame, corners);

			for (int i = 0, n = ids.size(); i < n; ++i)
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
				if(marker == NULL)
				{
					marker = create_marker_obj(R_cm, T_cm, id, cam);
					tree.add(marker);
				}
				else
				{
					update_cam_transform(R_cm, T_cm, cam, marker);
				}
				broadcast_tf(br, marker);
				broadcast_tf(br, cam);
			}
		}

		imshow("frame", frame);

		ros::spinOnce();
		if(waitKey(10) == 27) //27 == esc
			break;
	}
	
	return 0;
}

slam_obj *create_marker_obj(tf::Quaternion R_cm, tf::Vector3 T_cm, int id, slam_obj* camera)
{
	tf::Quaternion R_wc = camera->r;
	tf::Quaternion R_wm = R_wc * R_cm;

	tf::Vector3 T_wc = camera->t;
	tf::Vector3 T_wm = T_wc + (tf::Matrix3x3(R_wc) * T_cm);

	slam_obj *marker = new slam_obj;

	marker->id = id;
	marker->name = "id="+std::to_string(id);
	marker->r = R_wm;
	marker->t = T_wm;
	marker->left = NULL;
	marker->right = NULL;

	return marker;
}

void update_cam_transform(tf::Quaternion R_cm, tf::Vector3 T_cm ,slam_obj *camera, slam_obj *marker)
{
	tf::Vector3 T_wm = marker->t, T_wc = camera->t;
	tf::Quaternion R_wm = marker->r, R_wc = camera->r;

	T_wc = T_wm - (tf::Matrix3x3(R_wc) * T_cm);
	R_wc = R_wm * R_cm.inverse();

	camera->t = T_wc;
	camera->r = R_wc;
}

slam_obj *create_camera()
{
	slam_obj *camera = new slam_obj;

	camera->id = -1;
	camera->name = "c922";
	camera->r.setRPY(PI/2, PI, 0);
	camera->t = tf::Vector3(0, 0, 0);
	camera->left = NULL;
	camera->right = NULL;
	
	return camera;
}

void broadcast_tf(tf::TransformBroadcaster br, slam_obj *obj)
{
	tf::Transform transform;
	transform.setOrigin(obj->t);
	transform.setRotation(obj->r);
	br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), FIXED_FRAME, obj->name));
}
