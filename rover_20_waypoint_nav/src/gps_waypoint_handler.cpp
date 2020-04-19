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
#include <rover20_state_mach/RoverStateMsg.h>
#include <std_msgs/Bool.h>
#include <std_msgs/String.h>
#include <tf/transform_listener.h>
#include <math.h>


// initialize variables

typedef actionlib::SimpleActionClient <move_base_msgs::MoveBaseAction>
MoveBaseClient; //create a type definition for a client called MoveBaseClient

class GpsWaypoint
{
private:
  MoveBaseClient ac;

  ros::NodeHandle gw_nh;
  ros::Publisher sm_pub; //State machine publisher
  ros::Subscriber sm_sub; //State machine subscriber
  ros::Subscriber tg_sub; //Target GPS waypoint subscriber
  ros::Subscriber cg_sub; //Current GPS point subscriber 
  ros::Rate rate;

  rover20_state_mach::RoverStateMsg roverState;
  move_base_msgs::MoveBaseGoal moveBaseGoal;
  int count = 0, wait_count = 0;
  geometry_msgs::PointStamped UTM_point, map_point, UTM_next, map_next;
  double latiG, longG, latiC, longC, latiGT, longGT;
  std::string utm_zone;
  bool targetFlag = false; // flag for the activating waypoint handler

public:
    GpsWaypoint() : ac("move_base", true),
          sm_pub(gw_nh.advertise<std_msgs::String>("/gps_waypoint_handler/status", 10)), 
          sm_sub(gw_nh.subscribe<rover20_state_mach::RoverStateMsg>("/rover_state_topic",10, &GpsWaypoint::stateMachineCB, this)), //TODO:  convert to state machine msgs type and topic
          tg_sub(gw_nh.subscribe<sensor_msgs::NavSatFix>("/rover_gps/waypoint", 10, &GpsWaypoint::targetPointCB, this)),
          cg_sub(gw_nh.subscribe<sensor_msgs::NavSatFix>("/gps/fix", 10, &GpsWaypoint::currentPointCB, this)),
          rate(2)
  {
      while(!ac.waitForServer(ros::Duration(5.0)))
      {
          wait_count++;
          if(wait_count > 3)
          {
            ROS_ERROR("move_base action server did not come up, killing gps_waypoint_handler node...");
              // Notify joy_launch_control that waypoint following is complete
              std_msgs::Bool node_ended;
              node_ended.data = true;
              //pubWaypointNodeEnded.publish(node_ended); //TODO: send notification to state machine with same format
              ros::shutdown();
          }
          ROS_INFO("Waiting for the move_base action server to come up");
      }
      roverState.state = rover20_state_mach::RoverStateMsg::INITIALISE;
      std_msgs::String sm_info;
      sm_info.data = "0";
      sm_pub.publish(sm_info);
    }

  //Called once when the goal completes
  void doneCb(const actionlib::SimpleClientGoalState& state,
        const move_base_msgs::MoveBaseResultConstPtr& result)
  {
      ROS_INFO("Move base has reached its goal. ");
      //ROS_INFO("Answer: %i", result->sequence.back());
      //ros::shutdown();
    }

  // Called once when the goal becomes active
    void activeCb()
    {
      ROS_INFO("Goal just went active");
    }

    // Called every time feedback is received for the goal
    void feedbackCb(const move_base_msgs::MoveBaseFeedbackConstPtr& feedback)
    {
      //ROS_INFO("Got Feedback of move base ");
      //ROS_INFO("Got Feedback of length %lu", feedback->sequence.size());
      //geometry_msgs/PoseStamped base_position
    }

    void stateMachineCB(rover20_state_mach::RoverStateMsg rvrStt)
    {
      //ROS_INFO("Got Info from State Machine ");
      roverState.state = rvrStt.state;
    }

    void targetPointCB(sensor_msgs::NavSatFix targetPoint )
    {
      ROS_INFO("Got Info about target  ");
      //Gönderilen hedef koordinatları al. lat=long long=lat
      //check the message
      if (latiG != targetPoint.longitude)
      {
          latiG=targetPoint.longitude;
          longG=targetPoint.latitude;

          ROS_INFO("I got new target points");

          targetFlag = true;
    
          ROS_INFO("flag is :%s", targetFlag?"true":"false");
      }
      else 
      {
        ROS_WARN("Same target point has been sent. NO ACTION !");
      }
    }

    void currentPointCB(sensor_msgs::NavSatFix currentPoint )
    {
      //ROS_INFO("Got Info about current point ");
      longC=currentPoint.longitude;
      latiC=currentPoint.latitude;
    }

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
      if (calculateTemporaryError()>150 && ros::ok())
      {
        ROS_INFO("Created point error %f", calculateTemporaryError());
        createTempoaryPoint(latiGT, longGT);
      }
      else
      {
        return;
      }
    }

    void doStuff()
    {
      while(ros::ok())
      {
        if (roverState.state == rover20_state_mach::RoverStateMsg::READY)
        {
          if (targetFlag == true)
          {       
              double error = calculateError();
              ROS_INFO("I got the target point w error %f m", error);

              std_msgs::String sm_info;
              sm_info.data = "1";
              sm_pub.publish(sm_info);  //Send info to SM, we have sended goal to move base
          }
          else
          {
            ROS_INFO("Rover is ready for GPS waypoint navigation but there is no target point.\nSend target point.");
          }
        }

        else if (roverState.state == rover20_state_mach::RoverStateMsg::REACH_GPS)
        {
          ROS_INFO("adim0\n");

          if (targetFlag == true)
          {  
            ROS_INFO("adim1\n");

            if (calculateError()<150)         //(calculateError()<150) // distance to goal less than 150 m
            {
              ROS_INFO("adim2\n");

              while(true) // try to reach goal                            //>=5    calculateError() >=1
              {  
              ROS_INFO("adim3\n");
                moveBaseGoal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

                ac.sendGoal(moveBaseGoal);
      
                ROS_INFO("Rover is closer than 150m to goal with error: %f m, new goal has sended", calculateError());
                ac.waitForResult(ros::Duration(20)); 

                if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
                {
                  ROS_INFO("adim4\n");
                  ROS_INFO("Rover is closer than 150m to goal with error: %f m", calculateError()); 
                  if (calculateError() <=1)  //5
                  {
                    ROS_INFO("adim5\n");
                    ROS_INFO("Rover succeded!");
                    targetFlag = false;
                    std_msgs::String sm_info;
                    sm_info.data = "2";
                    sm_pub.publish(sm_info); 
                    ROS_INFO("flag is :%s", targetFlag?"true":"false");
                    break; //rover reached to actual goal SUCCESS!
                  }
                }
                else
                {
                  ros::Duration(20).sleep();              
                }
              }
            }

            else //if error bigger than 150 m
            {
              createTempoaryPoint(latiG, longG);
              while(calculateTemporaryError()>=80)  //5
              {
                moveBaseGoal = buildGoal(map_point, map_next); //initiate a move_base_msg called goal

                ac.sendGoal(moveBaseGoal,
                    boost::bind(&GpsWaypoint::doneCb, this, _1, _2),
                    boost::bind(&GpsWaypoint::activeCb, this),
                    boost::bind(&GpsWaypoint::feedbackCb, this, _1));
                ROS_INFO("Rover is far away 150 m from actual goal with error: %f m, temporary goal has sended", calculateError());
                ac.waitForResult(ros::Duration(10));
                if(ac.getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
                {
                  ROS_INFO("Rover has reached to temporary goal with error: %f m", calculateTemporaryError()); 
                  if (calculateTemporaryError() <=80)    //5
                  {
                    ROS_INFO("Rover has reached to temporary goal calculating again!");
                    break; //rover reached to actual goal SUCCES!
                  }
                }
                else
                {
                  ros::Duration(40).sleep();              
                }
              }
            }                      
          }
        }
        else  //Out of gps waypoint state, if there is an active goal from this node cancel it respect to
        {
          ROS_INFO("Not my turn bro :(");
        }
      rate.sleep();
      ros::spinOnce();
    }
      
  }
};
//***End of GpsWaypoint Class definition***

int main (int argc, char **argv)
{
    ros::init(argc, argv, "gps_waypoint_handler");
    GpsWaypoint waypointHandler;
    waypointHandler.doStuff();
    return 0;
}
