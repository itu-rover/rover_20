#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"

using namespace std;

double j1_angle;
double j2_angle;
double j3_angle;
double j4_angle;
double j5_angle;

double L1 = 7.0;
double L2 = 26.5;
double L3 = 27.3;
double L4 = 7.0;
double L5 = 20.0;

class coordinate{

public:

	double x;
	double y;
	double z;
	coordinate(double,double,double);
}

coordinate:coordinate(double new_x, double new_y, double new_z){

	x = new_x;
	y = new_y;
	z = new_z;
}


void j1_callback(const std_msgs::Float64::ConstPtr& msg){

    j1_angle = msg->data;
}

void j2_callback(const std_msgs::Float64::ConstPtr& msg){

    j2_angle = msg->data;
}

void j3_callback(const std_msgs::Float64::ConstPtr& msg){

    j3_angle = msg->data;
}

void j4_callback(const std_msgs::Float64::ConstPtr& msg){

    j4_angle = msg->data;
}

void j5_callback(const std_msgs::Float64::ConstPtr& msg){

    j5_angle = msg->data;
}


coordinate Dof_6(double t0, double t1, double t2, double t3, double t4){

	px = L4*(cos(t0)*cos(t1)*sin(t2) + cos(t0)*cos(t2)*sin(t1)) - L5*(cos(t4)*(sin(t0)*sin(t3) + cos(t3)*(cos(t0)*sin(t1)*sin(t2) - cos(t0)*cos(t1)*cos(t2))) - sin(t4)*(cos(t0)*cos(t1)*sin(t2) + cos(t0)*cos(t2)*sin(t1))) - L2*cos(t0)*sin(t1) + L3*cos(t0)*cos(t1)*cos(t2) - L3*cos(t0)*sin(t1)*sin(t2);
    py = L5*(cos(t4)*(cos(t0)*sin(t3) - cos(t3)*(sin(t0)*sin(t1)*sin(t2) - cos(t1)*cos(t2)*sin(t0))) + sin(t4)*(cos(t1)*sin(t0)*sin(t2) + cos(t2)*sin(t0)*sin(t1))) + L4*(cos(t1)*sin(t0)*sin(t2) + cos(t2)*sin(t0)*sin(t1)) - L2*sin(t0)*sin(t1) + L3*cos(t1)*cos(t2)*sin(t0) - L3*sin(t0)*sin(t1)*sin(t2);
    pz = L1 - L4*(cos(t1)*cos(t2) - sin(t1)*sin(t2)) + L2*cos(t1) - L5*(sin(t4)*(cos(t1)*cos(t2) - sin(t1)*sin(t2)) - cos(t3)*cos(t4)*(cos(t1)*sin(t2) + cos(t2)*sin(t1))) + L3*cos(t1)*sin(t2) + L3*cos(t2)*sin(t1);

    return coordinate(px,py,pz);
}

coordinate Dof_5(double t0, double t1, double t2){

	double px = L4*(cos(t0)*cos(t1)*sin(t2) + cos(t0)*cos(t2)*sin(t1)) - L2*cos(t0)*sin(t1) + L3*cos(t0)*cos(t1)*cos(t2) - L3*cos(t0)*sin(t1)*sin(t2);
    double py = L4*(cos(t1)*sin(t0)*sin(t2) + cos(t2)*sin(t0)*sin(t1)) - L2*sin(t0)*sin(t1) + L3*cos(t1)*cos(t2)*sin(t0) - L3*sin(t0)*sin(t1)*sin(t2);
    double pz = L1 - L4*(cos(t1)*cos(t2) - sin(t1)*sin(t2)) + L2*cos(t1) + L3*cos(t1)*sin(t2) + L3*cos(t2)*sin(t1);

    return coordinate(px,py,pz);
}

coordinate Dof_4(double t0, double t1, double t2){

	double px = L4*(cos(t0)*cos(t1)*sin(t2) + cos(t0)*cos(t2)*sin(t1)) - L2*cos(t0)*sin(t1) + L3*cos(t0)*cos(t1)*cos(t2) - L3*cos(t0)*sin(t1)*sin(t2);
    double py = L4*(cos(t1)*sin(t0)*sin(t2) + cos(t2)*sin(t0)*sin(t1)) - L2*sin(t0)*sin(t1) + L3*cos(t1)*cos(t2)*sin(t0) - L3*sin(t0)*sin(t1)*sin(t2);
    double pz = L1 - L4*(cos(t1)*cos(t2) - sin(t1)*sin(t2)) + L2*cos(t1) + L3*cos(t1)*sin(t2) + L3*cos(t2)*sin(t1);

    return coordinate(px,py,pz);
}
    
coordinate Dof_3(double t0, double t1, double t2){

	double px = L3*cos(t0)*cos(t1)*cos(t2) - L2*cos(t0)*sin(t1) - L3*cos(t0)*sin(t1)*sin(t2);
    double py = L3*cos(t1)*cos(t2)*sin(t0) - L2*sin(t0)*sin(t1) - L3*sin(t0)*sin(t1)*sin(t2);
    double pz = L1 + L2*cos(t1) + L3*cos(t1)*sin(t2) + L3*cos(t2)*sin(t1);

    return coordinate(px,py,pz);
}

coordinate Dof_2(double t0, double t1){

	double px = (-1)*L2*cos(t0)*sin(t1);
    double py = (-1)*L2*sin(t0)*sin(t1);
    double pz = L1 + L2*cos(t1);

    return coordinate(px,py,pz);
}

coordinate Dof_1(double t0){

	double px = 0.0;
    double py = 0.0; 
    double pz = L1;

    return coordinate(px,py,pz);
}

    
int main(int argc, char** argv){

	ros::init(argc, argv, "joints_pos_publisher");

	ros::NodeHandle j1_handle;
	ros::NodeHandle j2_handle;
	ros::NodeHandle j3_handle;
	ros::NodeHandle j4_handle;
	ros::NodeHandle j5_handle;

	ros::Subscriber j1_sub = j1_handle.subscribe("/rover_arm_j1_joint_position_controller/command",1,j1_callback);
	ros::Subscriber j2_sub = j2_handle.subscribe("/rover_arm_j2_joint_position_controller/command",1,j2_callback);
	ros::Subscriber j3_sub = j3_handle.subscribe("/rover_arm_j3_joint_position_controller/command",1,j3_callback);
	ros::Subscriber j4_sub = j4_handle.subscribe("/rover_arm_j4_joint_position_controller/command",1,j4_callback);
	ros::Subscriber j5_sub = j5_handle.subscribe("/rover_arm_j5_joint_position_controller/command",1,j5_callback);

	ros::Rate loop_rate(100);

	while(ros::ok()){

		ros::spinOnce();
		loop_rate.sleep();
	}
}
