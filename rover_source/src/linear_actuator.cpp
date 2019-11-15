#include <iostream>
#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/planning_scene_interface/planning_scene_interface.h>

//#include <moveit_msgs/DisplayRobotState.h>
//#include <moveit_msgs/DisplayTrajectory.h>

#include <moveit_msgs/AttachedCollisionObject.h>
#include <moveit_msgs/CollisionObject.h>

#include <moveit_visual_tools/moveit_visual_tools.h>

//quaternion
#include <tf2/LinearMath/Quaternion.h>
#include <tf/transform_datatypes.h>

//msgs
#include <sensor_msgs/Joy.h>
#include <geometry_msgs/Pose.h>

sensor_msgs::Joy joy_msg;
bool new_message = false;

void joystick_callback(const sensor_msgs::Joy::ConstPtr& msg)
{
    new_message = true;
    joy_msg = *msg;
    std::cout<<"data"<<std::endl;
}
int main(int argc, char* argv[])
{
    ros::init(argc, argv, "rover_arm_joystick_control");
    ros::NodeHandle node_handle;
    ros::AsyncSpinner spinner(2); //do we need these
    spinner.start();

    static const std::string PLANNING_GROUP = "eski";

    moveit::planning_interface::MoveGroupInterface move_group(PLANNING_GROUP);
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

    ros::Subscriber joy_sub = node_handle.subscribe("/joy",1,joystick_callback);

    while(ros::ok())
    {
        ros::spinOnce();
        if(!new_message) continue;
        //veriyi anla
        std::vector<geometry_msgs::Pose> waypoints;
        geometry_msgs::Pose current_pose;
        current_pose = move_group.getCurrentPose().pose;
        waypoints.push_back(current_pose);
        if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==1 && joy_msg.axes[1]!=0)   //roll --> x axis rotation
        {
            geometry_msgs::Pose target_pose = current_pose;

            tf::Quaternion q_orig, q_rot, q_new;
            double r= 0.17453 * joy_msg.axes[1] , p=0, y=0;
            q_rot = tf::createQuaternionFromRPY(r, p, y);

            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();                                                     //Turn the quaternion into x^2+y^2+z^2+w^2=1 form 
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();

        }
        else if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==0 && joy_msg.axes[0]!=0)    //pitch --> y axis rotation
        {
            geometry_msgs::Pose target_pose = current_pose;

            tf::Quaternion q_orig, q_rot, q_new;
            double r=0 , p= 0.17453 * joy_msg.axes[0], y=0;
            q_rot = tf::createQuaternionFromRPY(r, p, y);

            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();

        }
        else if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==0 && joy_msg.axes[1]!=0)    //yaw --> z axis rotation
        {
            geometry_msgs::Pose target_pose = current_pose;

            tf::Quaternion q_orig, q_rot, q_new;
            double r=0 , p=0, y= 0.17453 * joy_msg.axes[1];
            q_rot = tf::createQuaternionFromRPY(r, p, y);

            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();

        }

        new_message = false;

    }

    return 0;
}
