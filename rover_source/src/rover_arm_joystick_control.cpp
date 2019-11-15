#include <iostream>
#include <stdlib.h>
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
#include <sensor_msgs/JointState.h>
#include <geometry_msgs/Pose.h>
#include <std_msgs/Int8.h>

sensor_msgs::Joy joy_msg;
sensor_msgs::JointState state_msg;
bool new_message = false;
bool skip = false;

//std::cout<<msg->header.stamp<<std::endl;
//for(int i=0;i<msg->buttons.size();i++)
//{
//    std::cout<<msg->buttons[i]<<" ";
//}
//std::cout<<std::endl;


void joystick_callback(const sensor_msgs::Joy::ConstPtr& msg)
{

    new_message = true;
    joy_msg = *msg;
    std::cout<<"data"<<std::endl;

}

int main(int argc, char *argv[])
{
    ros::init(argc, argv, "rover_arm_joystick_control");
    ros::NodeHandle node_handle;
    ros::AsyncSpinner spinner(2); //do we need these
    spinner.start();

    static const std::string PLANNING_GROUP = "arm_rover";

    moveit::planning_interface::MoveGroupInterface move_group(PLANNING_GROUP);
    moveit::planning_interface::PlanningSceneInterface planning_scene_interface;

    ros::Subscriber joy_sub = node_handle.subscribe("/joy",1,joystick_callback);
    ros::Publisher gripper_command = node_handle.advertise<std_msgs::Int8>("/gripper_command19",10);
	
	
    while(ros::ok())
    {
		geometry_msgs::Pose current_pose;
		current_pose = move_group.getCurrentPose().pose;
		std::cout<<current_pose.position.x;
		std::cout<<current_pose.position.y;
		std::cout<<current_pose.position.z<<std::endl;
		
		if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		   fabs(current_pose.position.y+0.894225) < 0.05 &&
		   fabs(current_pose.position.z-0.612192) < 0.05)continue;
		//current_pose.position.y == && current_pose.position.z==) continue;
        
        std_msgs::Int8 gripper_msg;
        gripper_msg.data=2;
        ros::spinOnce();
        
        if(!new_message)
        {
            gripper_command.publish(gripper_msg);
            continue;
        }
        
        //veriyi anla
        std::vector<geometry_msgs::Pose> waypoints;
        
        
        //waypoints.push_back(current_pose);

        // GRIPPER


        if(joy_msg.buttons[2]==0 && joy_msg.buttons[0]==0)      // gripper steady
        {
            gripper_msg.data=2;
        }
        else if(joy_msg.buttons[2]==0 && joy_msg.buttons[0]==1) // close gripper
        {
            gripper_msg.data=0;
        }
        else if(joy_msg.buttons[2]==1 && joy_msg.buttons[0]==0) // open gripper
        {
            gripper_msg.data=1;
        }
        gripper_command.publish(gripper_msg);

        //  POSITION

        if(joy_msg.buttons[7]==0 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==0 && joy_msg.axes[1]!=0) //up & down
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.z += joy_msg.axes[1]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
			
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
			   fabs(current_pose.position.y+0.894225) < 0.05 &&
			   fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }
        
        else if(joy_msg.buttons[7]==0 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==0 && joy_msg.axes[1]!=0)
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.z += joy_msg.axes[1]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		    
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }



        else if(joy_msg.buttons[7]==0 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==0 && joy_msg.axes[0]!=0) //left & right
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.x += joy_msg.axes[0]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }
        
        else if(joy_msg.buttons[7]==0 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==0 && joy_msg.axes[0]!=0)
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.x += joy_msg.axes[0]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }



        else if(joy_msg.buttons[7]==0 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==1 && joy_msg.axes[1]!=0) //forward && backward
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.y += joy_msg.axes[1]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }
        
        else if(joy_msg.buttons[7]==1 && joy_msg.buttons[5]==0 && joy_msg.buttons[4]==1 && joy_msg.axes[1]!=0)
        {
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.position.y += joy_msg.axes[1]/10;
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }

        // ORIENTATION

        else if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==1 && joy_msg.axes[1]!=0)   //roll --> x axis rotation
        {
            geometry_msgs::Pose target_pose = current_pose;

            tf::Quaternion q_rot, q_new;
            double r=0 , p= 0, y=0;
			tf::Quaternion q_orig(current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w);
			tf::Matrix3x3(q_orig).getRPY(r,p,y);
			r += 2*0.15 * joy_msg.axes[1];
            q_rot = tf::createQuaternionFromRPY(r, p, y);
			/*
            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();
            * */

            target_pose.orientation.x = q_rot.getX();
            target_pose.orientation.y = q_rot.getY();
            target_pose.orientation.z = q_rot.getZ();
            target_pose.orientation.w = q_rot.getW();
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }

        }
        
        else if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==0 && joy_msg.axes[0]!=0)    //pitch --> y axis rotation
        {
            geometry_msgs::Pose target_pose = current_pose;
            double r=0 , p= 0, y=0;
			tf::Quaternion q_orig(current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w);
			tf::Matrix3x3(q_orig).getRPY(r,p,y);
			p += 2*0.15 * joy_msg.axes[0];
            tf::Quaternion  q_rot, q_new;
            q_rot = tf::createQuaternionFromRPY(r, p, y);
			/*
            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();
			*/

            target_pose.orientation.x = q_rot.getX();
            target_pose.orientation.y = q_rot.getY();
            target_pose.orientation.z = q_rot.getZ();
            target_pose.orientation.w = q_rot.getW();
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }
        }
        
        else if(joy_msg.buttons[5]==1 && joy_msg.buttons[4]==0 && joy_msg.axes[1]!=0)    //yaw --> z axis rotation
        {
            tf::Quaternion q_rot, q_new;
            double r=0 , p= 0, y=0;
			tf::Quaternion q_orig(current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w);
			tf::Matrix3x3(q_orig).getRPY(r,p,y);
			y += 2*0.15 * joy_msg.axes[1];
            q_rot = tf::createQuaternionFromRPY(r, p, y);
			/*
            quaternionMsgToTF(target_pose.orientation , q_orig);

            q_new = q_rot*q_orig;
            q_new.normalize();
            quaternionTFToMsg(q_new, target_pose.orientation);

            move_group.setPoseTarget(target_pose);
            moveit::planning_interface::MoveGroupInterface::Plan plan;
            move_group.move();
            * */
            geometry_msgs::Pose target_pose = current_pose;

            target_pose.orientation.x = q_rot.getX();
            target_pose.orientation.y = q_rot.getY();
            target_pose.orientation.z = q_rot.getZ();
            target_pose.orientation.w = q_rot.getW();
            waypoints.push_back(target_pose);

            moveit_msgs::RobotTrajectory trajectory;
            const double jump_threshold = 0.0;
            const double eef_step = 0.01;
            current_pose = move_group.getCurrentPose().pose;
		
            if(fabs(current_pose.position.x-0.110767) < 0.05 &&
		       fabs(current_pose.position.y+0.894225) < 0.05 &&
		       fabs(current_pose.position.z-0.612192) < 0.05) continue;
            
            double fraction = move_group.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
            ROS_INFO_NAMED("tutorial", "Visualizing plan 4 (Cartesian path) (%.2f%% acheived)", fraction * 100.0);
            
            if(fraction == 1){
				
                moveit::planning_interface::MoveGroupInterface::Plan plan;
                plan.trajectory_ = trajectory;
                move_group.execute(plan);
            }

        }

        new_message = false;

    }

    return 0;
}
