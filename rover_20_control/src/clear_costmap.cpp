#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <move_base/move_base.h>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <std_srvs/Empty.h>



int main(int argc, char** argv){

    ros::init(argc, argv, "service_client");
    ros::NodeHandle nh;

    

	ros::ServiceClient client = nh.serviceClient<std_srvs::Empty>("/move_base/clear_costmaps",true);
	std_srvs::Empty srv;

	if (client.call(srv)){
	  	ROS_INFO("Initiated gps_waypoint Subscribers");
	}
	

	ROS_INFO("END");

	
}
