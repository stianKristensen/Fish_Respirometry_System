#define ENCODER_OPTIMIZE_INTERRUPTS
// The above line forces the encoder library to default to using interrupt pins rather than using attachInterrupt leading to a more optimized code
#include <Encoder.h>
#include <MotorControl.h>
#include <PID_v1.h>

// ----PINS----
// Pump 1
int pump1_I1 = 1;
int pump1_I2 = 2;
int pump1_PWM = 3;

// Pump 2
int pump2_I1 = 6;
int pump2_I2 = 5;
int pump2_PWM = 4;

// Pump 3
int pump3_I1 = 7;
int pump3_I2 = 8;
int pump3_PWM = 9;

// Impeller Motor
int impeller_I1 = 16;
int impeller_I2 = 15;
int impeller_PWM = 14;

// Impeller Encoder
int impellerEnc_C2 = 17;
int impellerEnc_C1 = 18;

// SPI Communication
int chipSelect = 10;
int MOSIpin = 11;
int MISOpin = 12;
int CLKpin = 13;

// Other
int standbyPin = 0;

// ----CONSTANTS----
int encoderTicks = 45; //Number of ticks per rotation of the motor shaft
int revsPerCalc = 1; //Number of revolutions before RPM calculation is made
double impeller_Kp = 0.000001;
double impeller_Ki = 0.1;
double impeller_Kd = 0;

// ----INITIATE----
long impellerPos = -999;
long oldImpellerPos = 0;
double impellerRPM = 0;
double oldImpellerRPM = 0;
unsigned long timeCurrent = 0;
unsigned long timeElapsed = 0;
unsigned long timeOld = millis();
double impellerPWM = 0;
double impellerRPM_setpoint = 0;

Encoder impellerEnc(impellerEnc_C1,impellerEnc_C2);
MotorControl impeller(impeller_I1, impeller_I2, impeller_PWM);
PID impellerPID(&impellerRPM, &impellerPWM, &impellerRPM_setpoint, impeller_Kp, impeller_Ki, impeller_Kd, P_ON_M, DIRECT);

void setup() {
  Serial.begin(9600);
  impellerEnc.write(0);
  digitalWrite(standbyPin, HIGH);
  impeller.CW();
  impellerRPM_setpoint = 1000;
  impellerPID.SetMode(AUTOMATIC);

  impellerPID.Compute();
  impellerPWM = constrain(impellerPWM, 0, 255);
  impeller.DRIVE(impellerPWM);
  
}

void loop() {
  // ----PID----
  impellerPID.Compute();
  impellerPWM = constrain(impellerPWM, 0, 255);
  impeller.DRIVE(impellerPWM);
  
  impellerPos = impellerEnc.read();
  if (abs(impellerPos) >= (encoderTicks*revsPerCalc))
  {
    impellerEnc.write(0);
    timeCurrent = millis();
    timeElapsed = timeCurrent - timeOld;
    impellerRPM = (1000*60*revsPerCalc)/(timeElapsed);
    timeOld = timeCurrent;
    
    
  }
  
  if (impellerRPM != oldImpellerRPM) {
    Serial.print("Impeller RPM = ");
    Serial.print(impellerRPM);
    Serial.println();
    //Serial.print("Impeller PWM = ");
    //Serial.print(impellerPWM);
    //Serial.println();
    oldImpellerRPM = impellerRPM;
  }
  
}
