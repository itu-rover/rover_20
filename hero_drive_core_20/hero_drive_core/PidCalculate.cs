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
    public static class PidCalculate
    {
        public static double distance_totalError_sag_on = 0;
        public static double distance_totalError_sag_arka = 0;
        public static double distance_totalError_sol_arka = 0;
        public static double distance_totalError_sol_on = 0;
        public static double power;
        public static double pid_sag_on(double kP, double kI, double kD, double target)//////talon1
        {

            double distance_error;

            double k = (double)((IO.sag_on.GetSelectedSensorVelocity()));
            double enco_rpm = -(k / 1800);
            double target_rpm = target * 150;
            distance_error = (target_rpm) - enco_rpm;
            double distance_oldError = distance_error;
            if (target_rpm - 2 < distance_error && distance_error < target_rpm + 2)
            {
                power = target_rpm / 150;
            }

            else
            {
                distance_totalError_sag_on += distance_error;
                power = ((kP * distance_error) + (kI * (distance_totalError_sag_on)) + (kD * (distance_error - distance_oldError)));
            }


            Debug.Print(power.ToString());
            if (power > 50)
                power = 50;

            else if (power < -50)
                power = -50;


            return power;
        }
        public static double pid_sag_arka(double kP, double kI, double kD, double target)//////talon2
        {
            double power = 0;
            double distance_error;

            double enco_rpm;
            double k = (double)((IO.sag_arka.GetSelectedSensorVelocity()));
            enco_rpm = -(k / 252000);

            // Debug.Print((enco_rpm*100).ToString());
            //Debug.Print(power.ToString());
            distance_error = (target) - enco_rpm;
            double distance_oldError = distance_error;
            if (-0.0015 < distance_error && distance_error < 0.0015)
            {
                power = target;
            }

            else
            {
                distance_totalError_sag_arka += distance_error;
                power = ((kP * distance_error) + (kI * (distance_totalError_sag_arka)) + (kD * (distance_error - distance_oldError)));
            }



            if (power > 0.333)
                power = 0.333;

            else if (power < -0.333)
                power = -0.333;



            return power;
        }
        public static double pid_sol_on(double kP, double kI, double kD, double target)//////talon3
        {
            double power = 0;
            double distance_error;

            double enco_rpm;
            double k = (double)((IO.sol_on.GetSelectedSensorVelocity()));
            enco_rpm = (k / 252000);
            distance_error = (target) - enco_rpm;
            double distance_oldError = distance_error;
            if (-0.0015 < distance_error && distance_error < 0.0015)
            {
                power = target;
            }

            else
            {
                distance_totalError_sol_on += distance_error;
                power = ((kP * distance_error) + (kI * (distance_totalError_sol_on)) + (kD * (distance_error - distance_oldError)));
            }


            if (power > 0.333)
                power = 0.333;

            else if (power < -0.333)
                power = -0.333;

            return power;
        }
        public static double pid_sol_arka(double kP, double kI, double kD, double target)//////talon4
        {
            double power = 0;
            double distance_error;

            double enco_rpm;
            double k = (double)((IO.sol_arka.GetSelectedSensorVelocity()));
            enco_rpm = -(k / 252000);
            distance_error = (target) - enco_rpm;
            double distance_oldError = distance_error;
            if (-0.0015 < distance_error && distance_error < 0.0015)
            {
                power = target;
            }

            else
            {
                distance_totalError_sol_arka += distance_error;
                power = ((kP * distance_error) + (kI * (distance_totalError_sol_arka)) + (kD * (distance_error - distance_oldError)));
            }


            if (power > 0.333)
                power = 0.333;

            else if (power < -0.333)
                power = -0.333;


            return power;
        }

    }
}
