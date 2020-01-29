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
bool debug_mode;

geometry_msgs::PointStamped latLongtoUTM(double lati_input, double longi_input)
{
    double utm_x = 0, utm_y = 0;
    geometry_msgs::PointStamped UTM_point_output;

    //convert lat/long to utm
    RobotLocalization::NavsatConversions::LLtoUTM(lati_input, longi_input, utm_y, utm_x, utm_zone);

    //Construct UTM_point and map_point geometry messages
    UTM_point_output.header.frame_id = "utm";
    UTM_point_output.header.stamp = ros::Time(0);
    UTM_point_output.point.x = utm_x;
    UTM_point_output.point.y = utm_y;
    UTM_point_output.point.z = 0;

    return UTM_point_output;
}

geometry_msgs::PointStamped UTMtoMapPoint(geometry_msgs::PointStamped UTM_input)
{
    geometry_msgs::PointStamped map_point_output;
    bool notDone = true;
    tf::TransformListener listener; //create transformlistener object called listener
    ros::Time time_now = ros::Time::now();
    while(notDone)
    {
        try
        {
            UTM_point.header.stamp = ros::Time::now();
            listener.waitForTransform("odom", "utm", time_now, ros::Duration(3.0));
            listener.transformPoint("odom", UTM_input, map_point_output);
            notDone = false;
        }
        catch (tf::TransformException& ex)
        {
            ROS_WARN("%s", ex.what());
            ros::Duration(0.01).sleep();
            //return;
        }
    }
    return map_point_output;
}

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

void targetCallback (sensor_msgs::NavSatFix target)
{
    //Gönderilen hedef koordinatları al. lat=long long=lat
    //check the message
    if (latiG != target.longitude)
    {
        latiG=target.longitude;
        longG=target.latitude;

        ROS_INFO("I got new target points");

        flag = true;
    
        ROS_INFO("flag is :%s", flag?"true":"false");
    }

}

void currentCallback (sensor_msgs::NavSatFix current)
{

    longC=current.longitude;
    latiC=current.latitude;

    //ROS_INFO("I got to current points");
}

bool distanceChecker()
{   
    bool isItFar;
    ros::spinOnce();
    //Get current map points
    UTM_point = latLongtoUTM(latiC, longC);
    map_point = UTMtoMapPoint(UTM_point);

    UTM_next = latLongtoUTM(latiG, longG);
    map_next = UTMtoMapPoint(UTM_next);

    float error = sqrt((map_next.point.x-map_point.point.x)*(map_next.point.x-map_point.point.x)
        +(map_next.point.y-map_point.point.y)*(map_next.point.y-map_point.point.y));

    if (error > 150)
    {
        isItFar = false;
    }
    else
    {
        isItFar = true;
    }
    return isItFar;
}

float calculateError()
{
    //Get current map points
    UTM_point = latLongtoUTM(latiC, longC);
    map_point = UTMtoMapPoint(UTM_point);

    UTM_next = latLongtoUTM(latiG, longG);
    map_next = UTMtoMapPoint(UTM_next);

    float error = sqrt((map_next.point.x-map_point.point.x)*(map_next.point.x-map_point.point.x)
        +(map_next.point.y-map_point.point.y)*(map_next.point.y-map_point.point.y));    
    return error;
}

void writerResult(std::string path_to_result_file, float err)
{
    // Open file
    std::ofstream resultFile;
    resultFile.open (path_to_result_file.c_str(),std::ios::app);
    
    // Write to file
    resultFile << "Error: "<< err << " Target: " << std::fixed << latiG <<", " << std::fixed << longG << " Curent: " << std::fixed 
        << latiC << ", " << std::fixed << longC << std::endl;

    // Close file
    resultFile.close();
}


int main(int argc, char** argv)
{
    ros::init(argc, argv, "gps_waypoint"); //initiate node called gps_waypoint
    ros::NodeHandle n;
    ROS_INFO("Initiated gps_waypoint node");
    MoveBaseClient ac("/move_base", true);
    //construct an action client that we use to communication with the action named move_base.

    //ros::Publisher pubWaypointNodeEnded = n.advertise<std_msgs::Bool>("/outdoor_waypoint_nav/waypoint_following_status", 100);
    // arayüzü için üstteki yapıya benzer mantıkla mesaj atılabilir.

    //Initiate subscribers
    ros::Subscriber sub = n.subscribe("/rover_gps/waypoint", 10, targetCallback);
    ros::Subscriber sub1 = n.subscribe("/gps/fix", 10, currentCallback);

    ros::param::get("/outdoor_waypoint_nav/debug", debug_mode);

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

    ros::Rate r(2); // 2 hz

    while(ros::ok())
    {
        if (flag == true)
        {       
            ROS_INFO("Received current coordinates latitude:%.8f, longitude:%.8f", latiC, longC);
            ROS_INFO("Received goal coordinates latitude:%.8f, longitude:%.8f", latiG, longG);

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

            float error = 2;

            while(error >=1)
            {
                ac.waitForResult(ros::Duration(10));
                ros::spinOnce();
                error = calculateError(); 

                if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
                {
                    ROS_INFO("Rover has reached its goal! with error: %f m",error); 
                    if (error <= 1)
                    {
                        break;
                    }
                    else
                    {
                        goal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

                        // Send Goal
                        ROS_INFO("Goal calculated");
                        ac.sendGoal(goal);
                        ROS_INFO("Goal has sended"); 

                    }
                }//TODo: if error less than 20 meters wait less time
                else
                {
                    ROS_INFO("Wait 40 seconds");
                    ros::Duration(40).sleep();
                    ros::spinOnce();
                    error = calculateError();
                    ROS_INFO("Rover has not reached its goal! actual error is: %f m",error);

                    goal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

                    // Send Goal
                    ROS_INFO("Goal calculated");
                    ac.sendGoal(goal);
                    ROS_INFO("Goal has sended"); 
                }
            }         
/*
            if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
            {
                ROS_INFO("Rover has reached its goal!");
                ros::spinOnce();
                error = calculateError();
                ROS_INFO("Rover has reached its goal! with error: %f",error);

                
                if (debug_mode == true)
                {
                    std::string path =  ros::package::getPath("rover_waypoint_nav") + "/params/results.txt";
                    ROS_INFO("Writing results to file...");
                    ROS_INFO("Received current coordinates latitude:%.8f, longitude:%.8f", latiC, longC);
                    writerResult(path, error);
                }
                while (error >= 4)
                {
                    ros::spinOnce();

                    UTM_point = latLongtoUTM(latiC, longC);
                    map_point = UTMtoMapPoint(UTM_point);

                    UTM_next = latLongtoUTM(latiG, longG);
                    map_next = UTMtoMapPoint(UTM_next);
                    //Build goal to send to move_base
                    move_base_msgs::MoveBaseGoal goal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

                    // Send Goal
                    ROS_INFO("Error bigger than 4m, goal has sended again");
                    ac.sendGoal(goal); //push goal to move_base node

                    ROS_INFO("Wait for result");
                    ac.waitForResult();
                    error = calculateError();
                }
            }
            else
            {
                ROS_WARN("All is Well\n");
            }*/
            
            flag = false;
            ROS_INFO("flag is :%s", flag?"true":"false");
        }
        r.sleep();
        ros::spinOnce();
    }
    

    ROS_INFO("Rover SUCCEEDED!\n");

    return 0;
}
