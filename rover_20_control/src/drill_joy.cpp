//written by Çağatay Yürük 08.05.2018
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sensor_msgs/Joy.h>
#include <sstream>
#include <rover_control/Arm_msgs.h>
#include "math.h"

using namespace std;
float old_joint4=0;
float old_joint3=0;
class teleop_rover
{
public:
  teleop_rover();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);

  ros::NodeHandle nh_;

  int  axes1_,axes2_,switch1_,switch2_,switch3_,switch4_,X_,Y_,B_,A_;
  double scale_;
  ros::Publisher str_pub_, str_pub_1;
  ros::Subscriber joy_sub_;

  bool sent_disable_msg;
};


teleop_rover::teleop_rover():
 
  axes1_(1), //axes 1
  axes2_(4), //axes 2
 
  switch1_(4), //button LB
  switch2_(2),  //axes LT
  switch3_(5),  //button RB
  switch4_(5),  //axes RT
  Y_(3),
  X_(2),
  B_(1),
  A_(0),
  scale_(2.0)
{


  nh_.param("axes_1", axes1_, axes1_);
  nh_.param("axes_2", axes2_, axes2_);


  nh_.param("switch_1", switch1_, switch1_);
  nh_.param("switch_2", switch2_, switch2_);
  nh_.param("switch_3", switch3_, switch3_);
  nh_.param("switch_4", switch4_, switch4_);
  nh_.param("X", X_, X_);
  nh_.param("Y", Y_, Y_);
  nh_.param("B", B_, B_);
  nh_.param("A", A_, A_);
  nh_.param("scale", scale_, scale_);

  str_pub_ = nh_.advertise<rover_control::Arm_msgs>("/shovel_teleop", 1);
  str_pub_1 = nh_.advertise<rover_control::Arm_msgs>("/drill_teleop", 1);
  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy_drill", 1, &teleop_rover::joyCallback, this);

  sent_disable_msg = false;

}

void teleop_rover::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  
  rover_control::Arm_msgs arm_msg;
  rover_control::Arm_msgs arm_msg_1;
  
  if (joy->buttons[switch1_] && joy->buttons[switch3_])
  {    
    arm_msg_1.joint0=joy->axes[axes1_];
    arm_msg_1.joint2=joy->axes[axes2_];
    str_pub_1.publish(arm_msg_1);
  }
  else if (joy->buttons[switch1_])
  {    
    
    if(joy->buttons[Y_])
      arm_msg.joint0=-1;

    if (joy->buttons[A_])
      arm_msg.joint0=1;
    
    if(joy->buttons[X_])
      arm_msg.joint1=1;
    if (joy->buttons[B_])
      arm_msg.joint1=-1;
    
    arm_msg_1.joint0=joy->axes[axes1_];
    str_pub_1.publish(arm_msg_1);
    str_pub_.publish(arm_msg);
    sent_disable_msg = false;
  }
  
  else if (joy->axes[switch2_]<0)
  {    
    
    if(joy->buttons[Y_])
      arm_msg.joint2=-1;

    if (joy->buttons[A_])
      arm_msg.joint2=1;
    
    if(joy->buttons[X_])
      arm_msg.joint3=-1;
    if (joy->buttons[B_])
      arm_msg.joint3=1;

    str_pub_.publish(arm_msg);
    sent_disable_msg = false;
  }
  else if (joy->buttons[switch3_])
  {    
    
    if(joy->buttons[Y_])
      arm_msg.joint4=1;

    if (joy->buttons[A_])
      arm_msg.joint4=-1;
    
    if(joy->buttons[X_])
      arm_msg.joint5=-1;
    if (joy->buttons[B_])
      arm_msg.joint5=1;

    arm_msg_1.joint2=joy->axes[axes2_];
    str_pub_1.publish(arm_msg_1);
    str_pub_.publish(arm_msg);
    sent_disable_msg = false;
  }

  else if (joy->axes[switch4_]<0)
  {    
    
    if(joy->buttons[Y_])
      arm_msg.joint6=1;

    if (joy->buttons[A_])
      arm_msg.joint6=-1;
    
    
    str_pub_.publish(arm_msg);
    sent_disable_msg = false;
  }

  else if (joy->buttons[Y_])
  {    
    arm_msg_1.joint1=-joy->axes[axes1_];
  
    str_pub_1.publish(arm_msg_1);
    sent_disable_msg = false;
  }

  else
  {
    if (!sent_disable_msg)
    {
      str_pub_1.publish(arm_msg_1);
      str_pub_.publish(arm_msg);
      sent_disable_msg = true;
    }    
  }
  
}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "drill_rover");
  teleop_rover teleop_rover;

  ros::spin();
}
