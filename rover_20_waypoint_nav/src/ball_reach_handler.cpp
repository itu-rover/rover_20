#include <ros/ros.h>
#include <ros/package.h>
#include <fstream>
#include <utility>
#include <vector>
#include <move_base_msgs/MoveBaseAction.h>
#include <actionlib/client/simple_action_client.h>
#include <robot_localization/navsat_conversions.h>
#include <geometry_msgs/PointStamped.h>
#include <sensor_msgs/NavSatFix.h>
#include <std_msgs/Bool.h>
#include <tf/transform_listener.h>
#include <math.h>


// initialize variables

typedef actionlib::SimpleActionClient <move_base_msgs::MoveBaseAction>
MoveBaseClient; //create a type definition for a client called MoveBaseClient

geometry_msgs::PointStamped UTM_point, map_point, UTM_next, map_next;
int count = 0, wait_count = 0;
double latiG, longG, latiC, longC;
std::string utm_zone;
std::string path_local, path_abs;
bool flag = false; // flag for activate waypoint handler

 

move_base_msgs::MoveBaseGoal buildGoal(geometry_msgs::PointStamped map_point, geometry_msgs::PointStamped map_next)
{
    move_base_msgs::MoveBaseGoal goal;

    //Specify what frame we want the goal to be published in
    goal.target_pose.header.frame_id = "odom";
    goal.target_pose.header.stamp = ros::Time::now();

    // Specify x and y goal
    goal.target_pose.pose.position.x = map_next.point.x; //specify x goal !!changed to map_next from map_point
    goal.target_pose.pose.position.y = map_next.point.y; //specify y goal

    // Specify heading goal using current goal and next goal (point robot towards its next goal once it has achieved its current goal)
   
    tf::Matrix3x3 rot_euler;
    tf::Quaternion rot_quat;

    // Calculate quaternion
    float x_curr = map_point.point.x, y_curr = map_point.point.y; // set current coords.
    float x_next = map_next.point.x, y_next = map_next.point.y; // set coords. of next waypoint
    float delta_x = x_next - x_curr, delta_y = y_next - y_curr;   // change in coords.
    float yaw_curr = 0, pitch_curr = 0, roll_curr = 0;
    yaw_curr = atan2(delta_y, delta_x);

    // Specify quaternions
    rot_euler.setEulerYPR(yaw_curr, pitch_curr, roll_curr);
    rot_euler.getRotation(rot_quat);

    goal.target_pose.pose.orientation.x = rot_quat.getX();
    goal.target_pose.pose.orientation.y = rot_quat.getY();
    goal.target_pose.pose.orientation.z = rot_quat.getZ();
    goal.target_pose.pose.orientation.w = rot_quat.getW();


    return goal;
}

void targetCallback (std_msgs::String target)
{
    //Gönderilen hedef koordinatları al. lat=long long=lat
    //check the message

    std::string::size_type sz; 

    if (target_yaw != target.data)
    {   
        double target_yaw = std::stod (target.data,&sz);

        flag = true;
    
        ROS_INFO("flag is :%s", flag?"true":"false");
    }

}

void odomCallback (geometry_msgs::Odometry  odom)
{
    current_odom = odom.data;

}


int main(int argc, char** argv)
{
    ros::init(argc, argv, "ball_reach_handler"); //initiate node called gps_waypoint
    ros::NodeHandle n;
    ROS_INFO("Initiated gps_waypoint node");
    MoveBaseClient ac("/move_base", true);
    

    //ros::Publisher pubWaypointNodeEnded = n.advertise<std_msgs::Bool>("/outdoor_waypoint_nav/waypoint_following_status", 100);
    // arayüzü için üstteki yapıya benzer mantıkla mesaj atılabilir.

    //Initiate subscribers
    ros::Subscriber sub = n.subscribe("/rover_cam/heading", 10, targetCallback);
    ros::Subscriber sub1 = n.subscribe("/odometry/filtered", 10, odomCallback);

    ROS_INFO("Initiated gps_waypoint Subscribers");

    //wait for the action server to come up
    while(!ac.waitForServer(ros::Duration(5.0)))
    {
        wait_count++;
        if(wait_count > 3)
        {
            ROS_ERROR("move_base action server did not come up, killing gps_waypoint node...");
            // Notify joy_launch_control that waypoint following is complete
            std_msgs::Bool node_ended;
            node_ended.data = true;
            //pubWaypointNodeEnded.publish(node_ended);
            ros::shutdown();
        }
        ROS_INFO("Waiting for the move_base action server to come up");
    }

    ros::Rate r(1); // 1 hz

    while(ros::ok())
    {
        if (flag == true)
        {       
            ROS_INFO("Starting..");

            //Convert lat/long to utm:
            UTM_point = latLongtoUTM(latiC, longC);
            UTM_next = latLongtoUTM(latiG, longG);

            //Transform UTM to map point in odom frame
            map_point = UTMtoMapPoint(UTM_point);
            map_next = UTMtoMapPoint(UTM_next);

            //Build goal to send to move_base
            move_base_msgs::MoveBaseGoal goal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

            // Send Goal
            ROS_INFO("Sending goal");
            ac.sendGoal(goal); //push goal to move_base node

            //Wait for result //TODO: bizim hedef değişken olacağı için beklemiyoruz.
            //ROS_INFO("Wait for result");
            //ac.waitForResult(); //waiting to see if move_base was able to reach goal

            if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
                ROS_INFO("Rover has reached its goal!");
                //switch to next waypoint and repeat
            }
            else
            {
                ROS_WARN("All is Well\n");
            }
            
            flag = false;
            ROS_INFO("flag is :%s", flag?"true":"false");
        }
        r.sleep();
        ros::spinOnce();
    }
    

    ROS_INFO("Rover SUCCEEDED!\n");

    return 0;
}
