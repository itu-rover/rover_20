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
#include <std_srvs/Empty.h>

using namespace std;
// initialize variables
tf::TransformListener* listener;
typedef actionlib::SimpleActionClient <move_base_msgs::MoveBaseAction>
MoveBaseClient; //create a type definition for a client called MoveBaseClient


geometry_msgs::PointStamped UTM_point, map_point, UTM_next, map_next;
int count = 0, wait_count = 0;
double latiG, longG, latiC, longC, latiGT, longGT;
double goal_error;
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
    //create transformlistener object called listener
    ros::Time time_now = ros::Time::now();
    while(notDone)
    {
        try
        {
            UTM_point.header.stamp = ros::Time::now();
            listener->waitForTransform("odom", "utm", time_now, ros::Duration(3.0));
            listener->transformPoint("odom", UTM_input, map_point_output);
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
}

double calculateError()
{
    //Get current map points
    ros::spinOnce();
    UTM_point = latLongtoUTM(latiC, longC);
    map_point = UTMtoMapPoint(UTM_point);

    UTM_next = latLongtoUTM(latiG, longG);
    map_next = UTMtoMapPoint(UTM_next);
    double error = sqrt((map_next.point.x-map_point.point.x)*(map_next.point.x-map_point.point.x)
        +(map_next.point.y-map_point.point.y)*(map_next.point.y-map_point.point.y)); 
  
    return error;
}

double calculateTemporaryError()
{
    //Get current map points
    ros::spinOnce();
    UTM_point = latLongtoUTM(latiC, longC);
    map_point = UTMtoMapPoint(UTM_point);

    UTM_next = latLongtoUTM(latiGT, longGT);
    map_next = UTMtoMapPoint(UTM_next);

    double error = sqrt((map_next.point.x-map_point.point.x)*(map_next.point.x-map_point.point.x)
        +(map_next.point.y-map_point.point.y)*(map_next.point.y-map_point.point.y));    
    return error;
}

void createTempoaryPoint(double latiTarget, double longTarget)
{
    ROS_INFO("Creating new points between rover and %f, %f", latiTarget, longTarget);
    ros::spinOnce();
    double latiError = latiTarget - latiC, longError = longTarget - longC;
    latiGT = latiC + latiError/2;
    longGT = longC + longError/2;
    if (calculateTemporaryError()>50 && ros::ok())
    {
        ROS_INFO("Created point error %f", calculateTemporaryError());
        createTempoaryPoint(latiGT, longGT);
    }
    else
    {
        return;
    }
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
    tf::TransformListener rover_listener;
    listener = &rover_listener;
    ROS_INFO("Initiated gps_waypoint Subscribers");

    ros::ServiceClient costmap_client = n.serviceClient<std_srvs::Empty>("/move_base/clear_costmaps",true);
	std_srvs::Empty srv;


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

    ros::Rate r(10); // 2 hz

    while(ros::ok())
    {
        if (flag == true)
        {
            
            if (calculateError()<50) // distance to goal less than 150 m
            {
                
                while(true) // try to reach goal
                {   
                    
                    calculateError();
                    move_base_msgs::MoveBaseGoal goal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal
                    cout<<goal.target_pose.pose.position.x<<"  "<<map_next.point.x <<endl;
                    ac.sendGoal(goal);
                    ROS_INFO("Rover is closer than 50m to goal with error: %f m, new goal has sended", calculateError());
                    ac.waitForResult(ros::Duration(20)); //20 

                    if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
                    {
                        
                        ROS_INFO("Rover is closer than 50m to goal with error: %f m", calculateError()); 
                        if (calculateError() <=1)
                        {
                            ROS_INFO("Rover succeded!");
                            flag = false;
                            ROS_INFO("flag is :%s", flag?"true":"false");
                            break; //rover reached to actual goal SUCCES!
                        }
                    }//TODo: if error less than 20 meters wait less time
                    else
                    {
                        ros::Duration(20).sleep();  //40         
                    }

                    ros::spinOnce();
                }
            }
            else
            {
                createTempoaryPoint(latiG, longG);
                while(calculateTemporaryError()>=1)
                {
                    move_base_msgs::MoveBaseGoal goal = buildGoal(map_point, map_next);
                    ac.sendGoal(goal);
                    ROS_INFO("Rover is far away 50 m from actual goal with error: %f m, temporary goal has sended", calculateError());
                    ac.waitForResult(ros::Duration(20));
                    if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
                    {
                        ROS_INFO("Rover has reached to temporary goal with error: %f m", calculateTemporaryError()); 
                        if (calculateTemporaryError() <=1)
                        {
                            ROS_INFO("Rover has reached to temporary goal calculating again!");
                            break; //rover reached to actual goal SUCCES!
                        }
                    }
                    else
                    {
                        ros::Duration(20).sleep();  //40            
                    }
                }

            }
            if (costmap_client.call(srv)){
	  			ROS_INFO("Costmap is cleared");
			}                 
        }
        //ccr.runBehavior();
        r.sleep();
        ros::spinOnce();
    }
    return 0;
}