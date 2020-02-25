#include <Servo.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
Adafruit_BNO055 bno = Adafruit_BNO055(55);



Servo myservo;
const int SRV_1 = 9;
const int ISR = 2;
int a;
int cnt = 0;
int pos;
//volatile byte state = LOW;
volatile int x = 1;
String srl;
int len;
int i;
int j;
int first;
int last;
int posLib_1;
int posLib_2;
int posLib_3;
float ar_angle;


void readSerial() {
  srl = Serial.readString();
  len = srl.length();
  Serial.println(srl);

  for (i = 0; i < len; i++) {
    if (srl[i] == 'S' || srl[i] == 's' ) {
      for (j = i + 1; j < len; j++) {
        if (srl[j] == 'F' || srl[j] == 'f') {
          first = i;
          last = j;
          srl = srl.substring(first + 1, last);
          break;
        }
        if (isDigit(srl[j]) == false) {
          break;
        }
      }
    }
  }
}

void scanSRVlib() {
  Serial.flush();
  sensors_event_t event;
  boolean finished = true;
  
  for (posLib_1 = 60; posLib_1 < 120; posLib_1++) { 
    if (Serial.available()) {
      readSerial();
      if (srl.substring(1, 2) == "1") {
          bno.getEvent(&event);
          ar_angle = event.orientation.x;
          finished = false;
          for(int i =0 ; i<100; i++)
            Serial.println(ar_angle,4);
          break;
      }
    }
    myservo.write(posLib_1);
    delay(60);

    if (posLib_1 == 119) {

      for (posLib_2 = 120; posLib_2 > 0; posLib_2--) {
        if (Serial.available()) {
          readSerial();
          if (srl.substring(1, 2) == "1") {
            bno.getEvent(&event);
            ar_angle = event.orientation.x;
            finished = false;
            for(int i =0 ; i<100; i++)
              Serial.println(ar_angle,4);
            break;
          }
        }
        myservo.write(posLib_2);
        delay(60);

        if (posLib_2 == 1) {

          for (posLib_3 = 0; posLib_3 < 60; posLib_3++) {
            if (Serial.available()) {
              readSerial();
              if (srl.substring(1, 2) == "1") {
                bno.getEvent(&event);
                ar_angle = event.orientation.x;
                finished = false;
                for(int i =0 ; i<100; i++)
                  Serial.println(ar_angle,4);
                break;
              }
            }
            myservo.write(posLib_3);
            delay(60);

          }
        }
      }
    }
  }
  
  if (finished == false)
    return;
  
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  Serial.println("1");
  
}

void setup() {

  pinMode(SRV_1, OUTPUT);

  Serial.begin(9600);
  Serial.println("Orientation Sensor Test"); Serial.println("");

  myservo.attach(SRV_1);
  myservo.write(60);
  
  
  if (!bno.begin())
  {
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while (1);
  }
  
  delay(1000);
  bno.setExtCrystalUse(true);
}



void loop() {

  /*if (Serial.available()) {
    a = Serial.parseInt();
    Serial.println(a);
  }
s1
  /*Serial.print("X: ");
  Serial.print(event.orientation.x, 4);
  Serial.print("\tY: ");
  Serial.print(event.orientation.y, 4);
  Serial.print("\tZ: ");
  Serial.print(event.orientation.z, 4);
  Serial.println("");*/
  
  
  if (Serial.available()) {
    readSerial();
    Serial.println(srl);
    
    if (srl.substring(0, 1) == "1") {

      scanSRVlib();

    }
    else if (srl.substring(0, 1) == "0") {

      myservo.write(60);

    }

  }

  
}