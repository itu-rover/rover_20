#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include "definitions.h"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float64.h"
#include <sensor_msgs/Joy.h>

using namespace std;

bool new_message = false;

joy_message joy_msg;


void joystick_callback(const sensor_msgs::Joy::ConstPtr& msg)
{
    new_message = true;
    cout << msg->axes[0] << endl;
    joy_msg.set_axes(msg->axes[0],msg->axes[1],msg->axes[2],msg->axes[3],msg->axes[4],msg->axes[5]);
    joy_msg.set_buttons(msg->buttons[0],msg->buttons[1],msg->buttons[2],msg->buttons[3],msg->buttons[4],msg->buttons[5],msg->buttons[6],msg->buttons[7],msg->buttons[8],msg->buttons[9],msg->buttons[10],msg->buttons[11]);
}


int main(int argc, char **argv){

	vector<coordinate> my_joints;

	my_joints.push_back(coordinate(0.0,0.0,14.0));
	my_joints.push_back(coordinate(0.0,0.0,64.0));
	my_joints.push_back(coordinate(42.0,0.0,53.0));
	my_joints.push_back(coordinate(52.0,0.0,53.0));

	int i;
	double r, lambda;

	double link_lengths[3];

	link_lengths[0] = 50.0;							// link_2_3_length
	link_lengths[1] = 43.4165;						// link_3_5_length
	link_lengths[2] = 10.0;							// link_5_end_length

	ros::init(argc, argv, "talker");
	ros::NodeHandle n;
	ros::NodeHandle joint1_handle;
	ros::NodeHandle joint2_handle;
	ros::NodeHandle joint3_handle;
	ros::NodeHandle joint4_handle;
	ros::NodeHandle joint5_handle;
	ros::NodeHandle joint6_handle;
	ros::NodeHandle joy_handle;

	std_msgs::String angles;
	std_msgs::Float64 joint1_last;
	std_msgs::Float64 joint2_last;
	std_msgs::Float64 joint3_last;
	std_msgs::Float64 joint4_last;
	std_msgs::Float64 joint5_last;
	std_msgs::Float64 joint6_last;

	stringstream msg_ss;

	ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
	ros::Publisher joint1_pub = joint1_handle.advertise<std_msgs::Float64>("/rover_arm_eksen1_joint_position_controller/command", 1000);
	ros::Publisher joint2_pub = joint2_handle.advertise<std_msgs::Float64>("/rover_arm_eksen2_joint_position_controller/command", 1000);
	ros::Publisher joint3_pub = joint3_handle.advertise<std_msgs::Float64>("/rover_arm_eksen3_joint_position_controller/command", 1000);
	ros::Publisher joint4_pub = joint4_handle.advertise<std_msgs::Float64>("/rover_arm_eksen4_joint_position_controller/command", 1000);
	ros::Publisher joint5_pub = joint5_handle.advertise<std_msgs::Float64>("/rover_arm_eksen5_joint_position_controller/command", 1000);
	ros::Publisher joint6_pub = joint6_handle.advertise<std_msgs::Float64>("/rover_arm_eksen6_joint_position_controller/command", 1000);
	ros::Subscriber joy_sub = joy_handle.subscribe("/joy",1,joystick_callback);
	ros::Rate loop_rate(100);

	int count = 0;

	bool first_run = true;

	double X;
	double Y;
	double Z;

	double joint_1_angle;
	
	while(ros::ok()){

		ros::spinOnce();

		if(first_run){

			X = 0.0;
			Y = 0.0;
			Z = 0.0;

			joint_1_angle = 0.0;

			first_run = false;
		}

		if(joy_msg.get_button(5) == 1){

			X += joy_msg.get_axis(3) * 0.10;
			Y += joy_msg.get_axis(0) * 0.10;
			Z += joy_msg.get_axis(1) * 0.10;
		}

		else if(joy_msg.get_button(4) == 1){

			X += joy_msg.get_axis(3) * 0.02;
			Y += joy_msg.get_axis(0) * 0.02;
			Z += joy_msg.get_axis(1) * 0.02;
		}

		else{

			X += joy_msg.get_axis(3) * 0.06;
			Y += joy_msg.get_axis(0) * 0.06;
			Z += joy_msg.get_axis(1) * 0.06;
		}

		//cout << endl << "X: " << X << "  " << "Y: " << Y << "  " << "Z: " << Z << "  " << endl;

		coordinate new_end_point_pos = coordinate(52.0 + X, 0.0 + Y, 53.0 + Z);
		cout << endl << "Target: X = " << new_end_point_pos.get_x() << "  Y = " << new_end_point_pos.get_y() << "  Z = " << new_end_point_pos.get_z() << endl << endl;

		double joint_1_angle_dif = (-1.0)*joint_1_angle;

		coordinate reference_coord = coordinate(4,0,0);
		coordinate proj_joint_1 = coordinate(new_end_point_pos.get_x(), new_end_point_pos.get_y(), 0);
		joint_1_angle = angle_of_vectors(proj_joint_1, reference_coord);		// Projection of endpoint on xy and reference cord
		if(proj_joint_1.get_y() < 0) joint_1_angle = joint_1_angle * (-1);

		joint_1_angle_dif += joint_1_angle; 

		rotate_on_xy(my_joints[0], joint_1_angle_dif);
		rotate_on_xy(my_joints[1], joint_1_angle_dif);
		rotate_on_xy(my_joints[2], joint_1_angle_dif);
		rotate_on_xy(my_joints[3], joint_1_angle_dif);

		/*for(i = 0; i < 4; i++){

			cout << "The joint " << i << " position is: x = " << my_joints[i].get_x() << "  y = " << my_joints[i].get_y() << "  z = " << my_joints[i].get_z() << endl;
		}*/

		//FABRIK_algorithm(my_joints, link_lengths, new_end_point_pos);

		for(i = 0; i < 4; i++){

			cout << "The joint " << i+2 << " position is: x = " << my_joints[i].get_x() << "  y = " << my_joints[i].get_y() << "  z = " << my_joints[i].get_z() << endl;
		}

		cout << endl << endl;

		//cout << endl << endl;

		double joint_5_angle = find_angle(my_joints[2],my_joints[1],my_joints[3]);
		double joint_3_angle = find_angle(my_joints[1],my_joints[0],my_joints[2]);
		double joint_2_angle = find_angle(my_joints[0],coordinate(0.0,0.0,0.0),my_joints[1]);

		//cout << "Joint 5 narrow: " << cosinus_theorem(my_joints[3],my_joints[2],my_joints[4]) << endl;
		//cout << "Joint 3 narrow: " << cosinus_theorem(my_joints[2],my_joints[1],my_joints[3]) << endl;
		//cout << "Joint 2 narrow: " << cosinus_theorem(my_joints[1],my_joints[0],my_joints[2]) << endl << endl;


		//cout << "Joint 5: " << joint_5_angle << endl;
		//cout << "Joint 3: " << joint_3_angle << endl;
		//cout << "Joint 2: " << joint_2_angle << endl;

		//cout << "Joint 1: " << joint_1_angle << endl;
		//cout << joint_5_angle << endl;

		double joint_angles[5];

		joint_angles[0] = joint_1_angle;								// Calculated angles minus zero pos angles
		joint_angles[1] = 180.0 - joint_2_angle;
		joint_angles[2] = 90.0 - (joint_3_angle + 14.676352);
		joint_angles[3] = 90.0 - 90.0;
		joint_angles[4] = 270 - (joint_5_angle + 75.323648);

		msg_ss << joint_angles[0] << "  " << joint_angles[1] << "  " << joint_angles[2] << "  " << joint_angles[3] << "  " << joint_angles[4] << endl; 
		angles.data = msg_ss.str();

		cout << "Joint angles:  " << joint_angles[0] << "  " << joint_angles[1] << "  " << joint_angles[2] << "  " << joint_angles[3] << "  " << joint_angles[4] << endl;

		joint1_last.data = (joint_angles[0]*PI)/180; 
		joint2_last.data = (joint_angles[1]*PI)/180;
		joint3_last.data = (joint_angles[2]*PI)/180;
		joint4_last.data = (joint_angles[3]*PI)/180;
		joint5_last.data = (joint_angles[4]*PI)/180;
		joint6_last.data = 0.0;
	
		chatter_pub.publish(angles);
		joint1_pub.publish(joint1_last);
		joint2_pub.publish(joint2_last);
		joint3_pub.publish(joint3_last);
		joint4_pub.publish(joint4_last);
		joint5_pub.publish(joint5_last);
		joint6_pub.publish(joint6_last);
	 
	    loop_rate.sleep();
	    ++count;

	}

	return 0;


}