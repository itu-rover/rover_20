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
    public static class ScienceDrive
    {
        public static Boolean bt1_prev;
        public static Boolean bt1_current;
        public static Boolean bt2_prev;
        public static Boolean bt2_current;
        public static Boolean bt3_prev;
        public static Boolean bt3_current;
        public static Boolean bt4_prev;
        public static Boolean bt4_current;
        public static Boolean vacuum_on;
        public static Boolean faul_up;
        public static Boolean faul_down;

        public static void VacuumDrive()
        {


            if (IO._gamepad.GetButton(2))
            {
                IO.vacuum.Set(ControlMode.PercentOutput, 1);
                Debug.Print("vacuum on");
                Watchdog.Feed();
            }
            Thread.Sleep(5);
            if (IO._gamepad.GetButton(1))
            {
                IO.vacuum.Set(ControlMode.PercentOutput, 0);
                Debug.Print("vacuum off");
                Watchdog.Feed();
            }
            Thread.Sleep(5);


        }

        public static void BallScrewDrive()
        {



            double x = IO._gamepad.GetAxis(1);
            IO.faulhaber.Set(ControlMode.PercentOutput, x / 2);
            Debug.Print("faul up");
            Watchdog.Feed();

            Thread.Sleep(10);
        }
        public static void _kayar_hazne()
        {
            bt1_current = IO._gamepad.GetButton(1);
            if (bt1_current && !bt1_prev)
            {
                SerialCom.Write("S0010F");
                Debug.Print("sag ");
            }
            bt1_prev = bt1_current;

            bt2_current = IO._gamepad.GetButton(2);
            if (bt2_current && !bt2_prev)
            {
                SerialCom.Write("S0011F");
                Debug.Print("sol  ");
            }
            bt2_prev = bt2_current;
            bt3_current = IO._gamepad.GetButton(3);
            if (bt3_current && !bt3_prev)
            {
                SerialCom.Write("S0000F");
                Debug.Print("dur  ");
            }
            bt3_prev = bt3_current;

        }
        public static void _döner_hazne()
        {
            bt3_current = IO._gamepad.GetButton(3);
            if (bt3_current && !bt3_prev)
            {
                SerialCom.Write("S1000F");
                Debug.Print("dikey ");
            }
            bt3_prev = bt3_current;

            bt4_current = IO._gamepad.GetButton(4);
            if (bt4_current && !bt4_prev)
            {
                SerialCom.Write("S1100F");
                Debug.Print("yatay ");
            }
            bt4_prev = bt4_current;
        }
    }
}
