/*
  MotorControl, a simple library to control basic
  functions of the TB6612FNG motor driver.
*/

#include "Arduino.h"
#include "MotorControl.h"

MotorControl::MotorControl(int I1, int I2, int PWMpin)
{
  pinMode(I1, OUTPUT);
  pinMode(I2, OUTPUT);
  pinMode(PWMpin, OUTPUT);
  _I1 = I1;
  _I2 = I2;
  _PWMpin = PWMpin;
}

void MotorControl::CW()
{
  digitalWrite(_I1, HIGH);
  digitalWrite(_I2, LOW); 
}

void MotorControl::CCW()
{
  digitalWrite(_I1, LOW);
  digitalWrite(_I2, HIGH); 
}

void MotorControl::BRAKE()
{
  digitalWrite(_I1, HIGH);
  digitalWrite(_I2, HIGH); 
}

void MotorControl::COAST()
{
  digitalWrite(_I1, LOW);
  digitalWrite(_I2, LOW); 
}

void MotorControl::DRIVE(int PWMvalue)
{
  analogWrite(_PWMpin, PWMvalue); //PWMvalue between 0 and 255
}