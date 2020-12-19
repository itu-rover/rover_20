using System;
using Microsoft.SPOT;
using System.Threading;
using System.Text;

using CTRE.Phoenix;
using CTRE.Phoenix.Controller;
using CTRE.Phoenix.MotorControl.CAN;
using CTRE.Phoenix.Motion;
using CTRE.Phoenix.MotorControl;

namespace hero_drive_core
{
    class RoboticArmDrive
    {
        //public static int axis_no;
        //public static double thrust;
        //public static String axis_state;
        //public static Boolean bt4_prev = false;
        //public static Boolean bt4_current = false;
        //public static Boolean bt3_prev = false;
        //public static Boolean bt3_current = false;

        //public static void SelectAxis()
        //{
        //    bt4_current = IO._gamepad.GetButton(4);
        //    if (bt4_current && !bt4_prev)
        //    {                                
        //        axis_no++;
        //        Debug.Print("Axis No:");
        //    }
        //    bt4_prev = bt4_current;
        //    bt3_current = IO._gamepad.GetButton(3);
        //    if (bt3_current && !bt3_prev)
        //    {                            

        //        axis_no--;
        //        Debug.Print("Axis No:");
        //    }
        //    bt3_prev = bt3_current;
        //    if (IO._gamepad.GetButton(4) || IO._gamepad.GetButton(3))
        //    {
        //        if (axis_no % 8 == 1 || axis_no % 8 == -1)
        //        {
        //            axis_state = "1 joystick saga griper saga ";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 2 || axis_no % 8 == -2)
        //        {
        //            axis_state = "2 joystick saga griper cýkar ";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 3 || axis_no % 8 == -3)
        //        {
        //            axis_state = "3 joystick saga griper yukarý";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 4 || axis_no % 8 == -4)
        //        {
        //            axis_state = "4 joystick saga gripper saga ";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 5 || axis_no % 8 == -5)
        //        {
        //            axis_state = "5 joystick saga gripper assagý ";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 6 || axis_no % 8 == -6)
        //        {
        //            axis_state = "6 joystick saga saat yönünün tersi döner  ";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 7 || axis_no % 8 == -7)
        //        {
        //            axis_state = "7  joystick saga gripper acar  )";
        //            Debug.Print(axis_state);
        //        }
        //        else if (axis_no % 8 == 0)
        //        {
        //            Debug.Print("STANDBY");
        //        }

        //    }

        //}



        //public static void _Forward_Kinematic_Drive()
        //{

        //    SelectAxis();

        //    thrust = IO._gamepad.GetAxis(0) / 4;
        //    if (axis_no % 8 == 1 || axis_no % 8 == -1)
        //    {
        //        IO.axis_1.Set(ControlMode.PercentOutput, thrust);
        //    }
        //    else if (axis_no % 8 == 2 || axis_no % 8 == -2)
        //    {
        //        IO.axis_2.Set(ControlMode.PercentOutput, thrust);
        //    }
        //    else if (axis_no % 8 == 3 || axis_no % 8 == -3)
        //    {
        //        IO.axis_3.Set(ControlMode.PercentOutput, thrust);
        //    }
        //    else if (axis_no % 8 == 4 || axis_no % 8 == -4)
        //    {
        //        IO.axis_4.Set(ControlMode.PercentOutput, thrust);
        //    }
        //    else if (axis_no % 8 == 5 || axis_no % 8 == -5)
        //    {
        //        IO.axis_5.Set(ControlMode.PercentOutput, thrust);
        //    }
        //    else if (axis_no % 8 == 6 || axis_no % 8 == -6)
        //    {
        //        IO.axis_6.Set(ControlMode.PercentOutput, thrust*2);
        //    }
        //    else if (axis_no % 8 == 7 || axis_no % 8 == -7)
        //    {
        //        IO.gripper.Set(ControlMode.PercentOutput, thrust );
        //    }
        //}

        /*public static void DriveRoboticArm()
        {

            SelectAxis();
            ForwardKinematicDrive();

        }*/
        public static void _Forward_Kinematic_Drive()
        {

            if (IO._gamepad.GetButton(1) == true)
            {
                IO.axis_1.Set(ControlMode.PercentOutput, IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_1.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(2) == true)
            {
                IO.axis_2.Set(ControlMode.PercentOutput, -IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_2.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(3) == true)
            {
                IO.axis_3.Set(ControlMode.PercentOutput, -IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_3.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(4) == true)
            {
                IO.axis_4.Set(ControlMode.PercentOutput, IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_4.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(5) == true)
            {
                IO.axis_5.Set(ControlMode.PercentOutput, IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_5.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(6) == true)
            {
                IO.axis_6.Set(ControlMode.PercentOutput, IO._gamepad.GetAxis(1) / 4);
            }
            else
            {
                IO.axis_6.Set(ControlMode.PercentOutput, 0);
            }

            if (IO._gamepad.GetButton(12) == true)
            {
                IO.gripper.Set(ControlMode.PercentOutput, IO._gamepad.GetAxis(1) / 2);
            }
            else
            {
                IO.gripper.Set(ControlMode.PercentOutput, 0);
            }

            Thread.Sleep(10);
        }

    }
}

