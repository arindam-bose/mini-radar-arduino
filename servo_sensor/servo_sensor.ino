#include <Servo.h>
Servo myservo; 
int val = 0;              // variable to store the sensor value
int analogPin1 = A0;      // sensor1 pin
int analogPin2 = A1;      // sensor2 pin
String pval = "*";        // string variable to send sensor value over COM port

void setup() {
  Serial.begin(9600);     // setup serial communication
  myservo.attach(3);      // attach motor to PWM pin 3
  myservo.write(90);      // rotating motor to initial position
}

int calibrateValue(int pin) {
  int val = 100095*(pow(analogRead(pin),-0.966));   // sensor calibration equation
  if ((val>1500) || (val<0)){                       // disregarding erroneous readings
    val = NULL;
  }
  return val;
}

void readValue(int pos) {
  myservo.write(pos);                                   // rotating motor CW
  int val1 = calibrateValue(analogPin1);                    // sensor1 calibration equation
  int val2 = calibrateValue(analogPin2);                    // sensor2 calibration equation
  Serial.println(pos + pval + val1 + pval + val2);      // sending motor position and sensor reading over COM port
  delay(50);
}

void loop() {
  for(int i=0;i<=180;i=i+2){
    readValue(i);
  }
  for(int i=180;i>=0;i=i-2){
    readValue(i);
  }
}
