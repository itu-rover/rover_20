#include <ros.h>
#include <std_msgs/String.h>

#define sensor1 A0
int sensorValue1 = 1;

int sensor2 = A1;
int sensorValue2 = 0;
String str;
int sensor3 = A2;
int sensorValue3 = 0;

int sensor4 = A3;
int sensorValue4 = 0;

int sensor5 = A4;
int sensorValue5 = 0;

int sensor6 = A5;
int sensorValue6 = 0;
ros::NodeHandle nh;

std_msgs::String str_msg;
ros::Publisher chatter("chatter", &str_msg);

char finalChar[27];/*"S+processValue(sensorValue1)+ processValue(sensorValue2)+processValue(sensorValue3)+processValue(sensorValue4)+processValue(sensorValue5)+processValue(sensorValue6)";*/



void setup() {

  pinMode(sensor1, INPUT);
  pinMode(sensor2, INPUT);
  pinMode(sensor3, INPUT);
  pinMode(sensor4, INPUT);
  pinMode(sensor5, INPUT);
  pinMode(sensor6, INPUT);

  nh.initNode();
  nh.advertise(chatter);

  Serial.begin(57600); //115200
  String finalString = "";
}

void loop() {

  // read the value from the sensor:

 
  String finalString ;


  sensorValue1 = analogRead(sensor1);
  sensorValue2 = analogRead(sensor2);
  sensorValue3 = analogRead(sensor3);
  sensorValue4 = analogRead(sensor4);
  sensorValue5 = analogRead(sensor5);
  sensorValue6 = analogRead(sensor6);


  /*sensorValue1 = map(sensorValue1, 0, 1008, 0, 180);
  sensorValue2 = map(sensorValue2, 460, 675, 84, 15);
  sensorValue3 = map(sensorValue3, 710, 920, 104, 55);
  sensorValue4 = map(sensorValue4, 1008, 20, -90, 180) + 15;
  sensorValue5 = map(sensorValue5, 870, 550, 90, 0); */
  //sensorValue6 = map(sensorValue6,
  //sensorValue1 = constrain(sensorValue1, 0, 1008);
  //sensorValue2 = constrain(sensorValue2, 1079, 1193);
  //sensorValue3 = constrain(sensorValue3, 1268, 1139);
  //sensorValue4 = constrain(sensorValue4, 1140, 1125);
  //sensorValue5 = constrain(sensorValue5, 870, 550);

    
  /*sensorValue1 = map(sensorValue1, 0, 1008, 90, -90);
  sensorValue2 = map(sensorValue2, 786, 1020, 37.56, -39.53);
  sensorValue3 = map(sensorValue3, 20, 555, -47.45,81.06);
  sensorValue4 = map(sensorValue4, 352, 168, 2.86,-41.5);
  sensorValue5 = map(sensorValue5, 870, 550, 90, 0);
  sensorValue6 = 0 ; */

  //Serial.print("\n cak ");
  //Serial.print(sensorValue3);


  sensorValue1 = map(sensorValue1, 0, 1008, -90, 0);
  sensorValue2 = map(sensorValue2, 300, 0, 43.49, -47.44);
  sensorValue3 = map(sensorValue3, 520, 1023, -49.42,90.94);
  sensorValue4 = map(sensorValue4, 860, 559, -7.91,23.73);
  sensorValue5 = map(sensorValue5, 870, 550, 90, 0);
  sensorValue6 = 0 ;

  
 /*
  Serial.print(" 1 ");
  Serial.print(processValue(sensorValue1));
  //Serial.print(" 2 ");
  //Serial.print(processValue(sensorValue2));
  Serial.print(" 3 ");
  Serial.print(sensorValue3);
  Serial.print(" 3 ");
  Serial.print(processValue(sensorValue3));
  //Serial.println(sensorValue3);
  Serial.print(" 4 ");
  Serial.print(sensorValue4);
  Serial.print(" 4 ");
  Serial.print(processValue(sensorValue4));
  //Serial.print(" 5 ");
  //Serial.print(processValue(sensorValue5));
  //Serial.print(" 6 ");
  //Serial.print(processValue(sensorValue6));
  //Serial.print(" ");
  */
  //Serial.print(processValue(sensorValue4));/*processValue(sensorValue2)+processValue(sensorValue3)+processValue(sensorValue4)+processValue(sensorValue5)+"0000F\r\n";
  //finalString = "S" + processValue(sensorValue1) + processValue(sensorValue2) + "  " + String(sensorValue3) + "  " + processValue(sensorValue4) + processValue(sensorValue5) + "0000F\r\n";
  finalString = "S"+processValue(sensorValue1)+processValue(sensorValue2)+processValue(sensorValue3)+processValue(sensorValue4)+processValue(sensorValue5)+processValue(sensorValue6)+"C"+"F" ;

  //Serial.print(finalString);
  //Serial.println(finalString);

  

  // int str_len = finalString.length() + 1 ;
    
  finalString.toCharArray(finalChar, 27);
  
 
  
  str_msg.data = finalChar;
  chatter.publish( &str_msg );
  nh.spinOnce();
  delay(40);

  
}

String processValue(int value) {

  String valueString = "0000";

  if (value < 0)
  {
    if (value > -10)                      // -9 , -1
    {
      valueString = "000" + String(abs(value));
    }
    else if ((value <= -10) && (value > -100))   // -99,-10
    {
      valueString = "00" + String(abs(value));
    }
    else                                        // -999,-11
    {
      valueString = "0" + String(abs(value));
    }
  }

  else if (value > 0)
  {
    if (value < 10)                           //1, 9
    {
      valueString = "100" + String(value);
    }
    else if ((value >= 10) && (value < 100))  //10, 99
    {
      valueString = "10" + String(value);
    }
    else
    {
      valueString = "1" + String(value);
    }
  }
  else
  {
    valueString = "0000";
  }
  return valueString;
}
