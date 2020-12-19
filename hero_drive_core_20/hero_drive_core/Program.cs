using System;
using System.Threading;
using Microsoft.SPOT;
using System.Text;


using CTRE.Phoenix;
using CTRE.Phoenix.Controller;
using CTRE.Phoenix.MotorControl.CAN;
using CTRE.Phoenix.Motion;
using CTRE.Phoenix.MotorControl;

namespace hero_drive_core
{
    public class Program
    {

        public static void Main()
        {
            InitAndLoop.Init();
            InitAndLoop.Loop();

        }

    }
}