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
    class SerialCom
    {
        public static System.IO.Ports.SerialPort _uart = new System.IO.Ports.SerialPort(CTRE.HERO.IO.Port1.UART, 115200);
        public static byte[] _rx = new byte[1024];
        public static int readCnt;
        public static int sag_motors = 0;
        public static int sol_motors = 0;
        public static int k;
        public static bool test_1;
        public static bool test_2;
        public static int test_3;
        public static byte[] SD_byt = new byte[1024];
        public static int[] SD_int = new int[1024];

        public static string Read()
        {
            if (_uart.BytesToRead > 0)
            {
                readCnt = _uart.Read(_rx, 0, 1024);
            }

            return new string(Encoding.UTF8.GetChars(_rx));
        }

        public static void Write(string msg)
        {
            // _uart.Open();
            byte[] msg_byte = String2Byte(msg);

            _uart.Write(msg_byte, 0, msg.Length);
            Thread.Sleep(50);



        }

        public static byte[] String2Byte(String msg) // Bunu biz yazdýk ha
        {
            byte[] retval = new byte[msg.Length];
            for (int i = 0; i < msg.Length; ++i)
                retval[i] = (byte)msg[i];
            return retval;
        }

        public static void Serial_extract()
        {
            Debug.Print("**********************************************************");
            Debug.Print("----------------");

            for (int i = 0; i < SerialCom.Read().Length; ++i)
                SD_byt[i] = (byte)SerialCom.Read()[i];
            for (int i = 0; i < SerialCom.Read().Length; i++)
            {
                SD_int[i] = (SD_byt[i]) - 48;

            }

            for (int i = 0; i < SerialCom.Read().Length; i++)
            {

                if (SD_int[i] == 35 && SD_int[i + 9] == 22)
                {
                    test_1 = true;
                    k = i;
                }
                if (test_1 == true)
                    break;
            }
            if (test_1 == true)
            {
                for (int i = 0; i < 8; i++, k++)
                {
                    SD_int[i] = SD_int[k + 1];
                }
                test_2 = true;
            }
            if (test_2 == true)
            {

                for (int i = 0; i < 8; i++)
                {
                    if (SD_int[i] >= 0 && SD_int[i] <= 9)
                        test_3++;
                }

            }
            if (test_3 == 8)
            {
                Debug.Print("----------------");

                sag_motors = (SD_int[1] * 100 + SD_int[2] * 10 + SD_int[3]);
                sol_motors = (SD_int[5] * 100 + SD_int[6] * 10 + SD_int[7]);


                if (SD_int[0] == 0)
                {
                    sag_motors *= -1;
                }
                if (SD_int[4] == 0)
                {
                    sol_motors *= -1;
                }


                if (sag_motors < -255 && sag_motors > 255)
                    sag_motors = 0;
                if (sol_motors < -255 && sol_motors > 255)
                    sol_motors = 0;


            }

        }



    }
}

