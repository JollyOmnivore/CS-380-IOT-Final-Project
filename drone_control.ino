#include "ICM_20948.h" // Click here to get the library: http://librarymanager/All#SparkFun_ICM_20948_IMU
#include "Wire.h"

ICM_20948_I2C myICM;

int switchState;
int down;
int up;

enum state{
  droneOn,
  droneOff
};

state currState = droneOff;

void setup() {
  Serial.begin(9600);

  pinMode(7, INPUT);
  pinMode(10, INPUT);
  pinMode(12, INPUT);
  Wire.begin();


 myICM.begin(Wire, 1);

}

void loop() {
  switch(currState){
    case droneOff:
      if (myICM.dataReady()){
        down = digitalRead(12);
        up = digitalRead(13);
        if(up == HIGH && down == HIGH){
          Serial.println("TAKE OFF");
          delay(1000);
          currState = droneOn;
          break;
        }
      }
      break;

    case droneOn:
      down = digitalRead(12);
      up = digitalRead(13);
      switchState = digitalRead(7);

      if(up == HIGH && down == HIGH){
        Serial.println("LAND");
        currState = droneOff;
        delay(3000);
      }

      else if(down == HIGH && up == LOW){
        Serial.println("DOWN");
        delay(1000);
      }
      else if(up == HIGH && down == LOW){
        Serial.println("UP");
        delay(1000);
      }

      if (myICM.dataReady()){
        myICM.getAGMT();  
        if(myICM.gyrY() >= 100){
          Serial.println("FLY FORWARD");
          delay(1000);
        }
        else if(myICM.gyrZ() >= 100){
          Serial.println("ROTATE COUNTER CLOCKWISE");
          delay(1000);
        }
        else if(myICM.gyrZ() <= -100){
          Serial.println("ROTATE CLOCKWISE");
          delay(1000);
        }
        else if(myICM.gyrY() <= -100){
          Serial.println("FLY BACKWARDS");
          delay(1000);
        }
        else if(myICM.gyrX() <= -100){
          Serial.println("FLY LEFT");
          delay(1000);
        }
        else if(myICM.gyrX() >= 100){
          Serial.println("FLY RIGHT");
          delay(1000);
        }
        else if(myICM.temp() >= 70){
          Serial.println("Emergency landing due to temperature");
          currState = droneOff;
        }
      }
      break;
  }

}
