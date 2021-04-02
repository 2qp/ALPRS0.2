#include <Servo.h>
Servo myservo; 
String inByte;
int pos;

void setup() {
 
  myservo.attach(8);
  Serial.begin(9600);
  myservo.write(0);
}

void loop()
{    
  if(Serial.available())
    { 
    inByte = Serial.readStringUntil('\n');
    for(pos = 0; pos < 90; pos +=1)
      {
        myservo.write(pos);
        delay(30);
      }
      
    delay(5000);
    
    for(pos = 90; pos > 1; pos -=1)
      {
        myservo.write(pos);
        delay(30);
      }
      
    }
}

