/*
  MotorControl, a simple library to control basic
  functions of the TB6612FNG motor driver.
*/
#ifndef MotorControl_h
#define MotorControl_h

#include "Arduino.h"

class MotorControl
{
  public:
    MotorControl(int I1, int I2, int PWMpin);
    void CW();
    void CCW();
    void BRAKE();
    void COAST();
    void DRIVE(int PWMvalue);
  private:
    int _I1, _I2, _PWMpin;
};

#endif