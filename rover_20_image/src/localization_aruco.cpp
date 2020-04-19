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

#define PI 3.14159265358979323846
#define FIXED_FRAME "aruco_slam_map"

using namespace cv;
using namespace aruco;

/* 
	Binary tree structure for objects of slam system
	According to aruco, every marker has uniqe id for
	every marker. Ids represented as integers starting from 0
	Hence in this structure:
	id -1      -> camera
	id non -1  -> artag
*/
struct slam_obj 
{
	int id;
	std::string name; 

	tf::Quaternion r;
	tf::Vector3 t;

	slam_obj *left;
	slam_obj *right;
};

slam_obj *add(slam_obj *root, slam_obj *new_obj)
{
	if(root == NULL)
		return new_obj;

	if(new_obj->id > root->id)
		root->right = add(root->right, new_obj);
	else
		root->left = add(root->left, new_obj);

	return root;
}

slam_obj *search_id(slam_obj *root, int id)
{
	if(root->id == id || root == NULL)
		return root;

	if(root->id > id)
		return search_id(root->left, id);
	else
		return search_id(root->right, id);
}

slam_obj *create_marker_obj(tf::Quaternion R_cm, tf::Vector3 T_cm, int id, slam_obj* camera)
{
	tf::Quaternion R_wc = camera->r;
	tf::Quaternion R_wm = R_wc * R_cm;

	tf::Vector3 T_wc = camera->t;
	tf::Vector3 T_wm = T_wc + (tf::Matrix3x3(R_wc) * T_cm);

	slam_obj *marker = (slam_obj*)malloc(sizeof(slam_obj));
	marker->id = id;
	marker->name = "id="+std::to_string(id);
	marker->r = R_wm;
	marker->t = T_wm;
	marker->left = NULL;
	marker->right = NULL;

	return marker;
}

void update_cam_transform(slam_obj *camera, slam_obj *marker)
{
	

}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "localization_aruco");

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

    //custom stuff
    slam_obj *map = NULL;

    slam_obj *camera = (slam_obj*)malloc(sizeof(slam_obj));
    camera->id = -1;
    camera->name = "c922";
    camera->r.setRPY(PI/2, 0, 0);
    camera->t = tf::Vector3(0, 0, 0);
    camera->left = NULL;
    camera->right = NULL;

    map = add(map, camera);


	cap.open(1);

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


		for(auto& id : ids)
		{
			std::cout << id;
		}


		if(ids.size() > 0)
		{	
			slam_obj *cam = search_id(map, -1);

			drawDetectedMarkers(frame, corners);

			for (int i = 0, n = ids.size(); i < n; ++i)
			{
				int id = ids[i];
				Vec3d r = rvecs[i];
				Vec3d t = tvecs[i];

				drawAxis(frame, mtx, dist, r, t, 0.1);

				slam_obj *marker = search_id(map, id);

				// If marker is not exist in map(slam system) we will add it
				if(marker == NULL)
				{	
					/*
					marker = create_marker_obj(R_cm, T_cm, camera);
					tf::Transform transform;

					tf::Vector3 v;
					tf::Quaternion q;

					v = tf::Vector3(t[0],t[1],t[2]);
					q.setRPY(r[0], r[1], r[2]);

					transform.setOrigin(t);
					transform.setRotation(q);

					br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), FIXED_FRAME, "artag"));
					*/
				}
			}
		}

		imshow("frame", frame);

		ros::spinOnce();
		if(waitKey(10) == 27) //27 == esc
			break;
	}

	return 0;
}
