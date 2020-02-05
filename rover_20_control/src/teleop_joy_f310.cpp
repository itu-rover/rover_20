//written by Çağatay Yürük 08.05.2018
#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>

using namespace std;
class teleop_rover
{
public:
  teleop_rover();

private:
  void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);

  ros::NodeHandle nh_;

  int linear_, angular_,turbo_,kill_;
  double turbo_scale;
  ros::Publisher vel_pub_;
  ros::Subscriber joy_sub_;

  bool sent_disable_msg;
};


teleop_rover::teleop_rover():
  linear_(1),
  angular_(0),
  turbo_(5),
  kill_(2),
  turbo_scale(2.0)
{

  nh_.param("axis_linear", linear_, linear_);
  nh_.param("axis_angular", angular_, angular_);
  nh_.param("turbo", turbo_, turbo_);
  nh_.param("kill", kill_, kill_);
  nh_.param("turbo_scale", turbo_scale, turbo_scale);

  //vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/rover_joy/cmd_vel", 1);
  vel_pub_ = nh_.advertise<geometry_msgs::Twist>("/joy_teleop/cmd_vel", 1);


  joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 1, &teleop_rover::joyCallback, this);

  sent_disable_msg = false;

}

void teleop_rover::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
  geometry_msgs::Twist twist;
  if (joy->buttons[kill_])
  {    
    twist.angular.z = joy->axes[angular_]*0.5; //TODO: scale ekle
    twist.linear.x = joy->axes[linear_]*0.5;
    vel_pub_.publish(twist);
    sent_disable_msg = false;
  }
  else if (joy->buttons[turbo_])
  {
    twist.angular.z = turbo_scale*joy->axes[angular_]; //TODO: scale ekle
    twist.linear.x = turbo_scale*joy->axes[linear_];
    vel_pub_.publish(twist);
    sent_disable_msg = false;
  }
  else
  {
    if (!sent_disable_msg)
    {
      vel_pub_.publish(twist);
      sent_disable_msg = true;
    }    
  }
  

}


int main(int argc, char** argv)
{
  ros::init(argc, argv, "teleop_rover");
  teleop_rover teleop_rover;

  ros::spin();
}
