/*
  Cludge_Servo
  Author: Shawn Hymel
  Date: April 21, 2014
  
  This is a basic servo control over Serial. Send 0-179 over UART.
*/

#include <Servo.h>

// Global variables
Servo servo;
int servo_pin = 9;
int pos = 90;

// Init UART and servo
void setup() {
  Serial.begin(9600);
  servo.attach(servo_pin);
}

// As UART commands come in, send to servo
void loop() {
  if (Serial.available()) {
    uint8_t b = Serial.read();
    if (b > 180) {
      b = 180;
    }
    servo.write(b);
  }
}

