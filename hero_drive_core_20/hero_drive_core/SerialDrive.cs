using System;
using Microsoft.SPOT;
using System.Threading;
using System.Text;


using CTRE.Phoenix;
using CTRE.Phoenix.Controller;
using CTRE.Phoenix.MotorControl;
using CTRE.Phoenix.MotorControl.CAN;

namespace hero_drive_core
{
    class SerialDrive
    {
        public static double sag_motors_pass = 0;
        public static double sol_motors_pass = 0;



        public static void Serial_drive()
        {
            IO.sag_on.SetInverted(true);
            IO.sol_on.SetInverted(true);
            if (SerialCom.sag_motors < -255 || SerialCom.sag_motors > 255 || SerialCom.sol_motors < -255 || SerialCom.sol_motors > 255)
            {
                SerialCom.sag_motors = 0;
                SerialCom.sol_motors = 0;
            }

            if (sag_motors_pass < SerialCom.sag_motors && sol_motors_pass < SerialCom.sol_motors)
                for (; sag_motors_pass <= SerialCom.sag_motors && sol_motors_pass <= SerialCom.sol_motors; sag_motors_pass++, sol_motors_pass++)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass < SerialCom.sag_motors && sol_motors_pass > SerialCom.sol_motors)
                for (; sag_motors_pass <= SerialCom.sag_motors && sol_motors_pass >= SerialCom.sol_motors; sag_motors_pass++, sol_motors_pass--)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass > SerialCom.sag_motors && sol_motors_pass < SerialCom.sol_motors)
                for (; sag_motors_pass >= SerialCom.sag_motors && sol_motors_pass <= SerialCom.sol_motors; sag_motors_pass--, sol_motors_pass++)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass > SerialCom.sag_motors && sol_motors_pass > SerialCom.sol_motors)
                for (; sag_motors_pass >= SerialCom.sag_motors && sol_motors_pass >= SerialCom.sol_motors; sag_motors_pass--, sol_motors_pass--)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }

            if (sag_motors_pass == SerialCom.sag_motors && sol_motors_pass > SerialCom.sol_motors)
                for (; sag_motors_pass == SerialCom.sag_motors && sol_motors_pass <= SerialCom.sol_motors; sol_motors_pass++)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass == SerialCom.sag_motors && sol_motors_pass < SerialCom.sol_motors)
                for (; sag_motors_pass == SerialCom.sag_motors && sol_motors_pass <= SerialCom.sol_motors; sol_motors_pass--)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass > SerialCom.sag_motors && sol_motors_pass == SerialCom.sol_motors)
                for (; sag_motors_pass >= SerialCom.sag_motors && sol_motors_pass == SerialCom.sol_motors; sag_motors_pass--)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass > SerialCom.sag_motors && sol_motors_pass == SerialCom.sol_motors)
                for (; sag_motors_pass >= SerialCom.sag_motors && sol_motors_pass == SerialCom.sol_motors; sag_motors_pass--)
                {
                    IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                    IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                    Watchdog.Feed();
                }
            if (sag_motors_pass == SerialCom.sag_motors && sol_motors_pass == SerialCom.sol_motors)

            {
                IO.sag_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                IO.sag_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sag_motors_pass / 600));
                IO.sol_on.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                IO.sol_arka.Set(ControlMode.PercentOutput, PidCalculate.pid_sag_arka(0.15, 0.01, 0.1, sol_motors_pass / 600));
                Watchdog.Feed();
            }


        }
    }
}
