


#define IN1 PA8
#define IN2 PA9
#define SLEEPn PB3
#define USR_BTN PC13
#define V_REF PA4
#define AIOUT PC1
#define R_SENSE 0.01

#include <Wire.h>
#include <VL6180X.h>
#define pinSDA PB_7_ALT1
#define pinSCL PC6

VL6180X sensor;

void initPhysics()
{
  pinMode(SLEEPn, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(V_REF, OUTPUT);
  pinMode(AIOUT, INPUT_PULLDOWN);

  digitalWrite(SLEEPn, HIGH);
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);

  analogWrite(V_REF, 255);

  Wire.setSDA(pinSDA);
  Wire.setSCL(pinSCL);
  Wire.begin();
  
  sensor.init();
  sensor.configureDefault();
  sensor.setTimeout(500);

  analogWriteFrequency(20000);
}

int get_height()
{
  return sensor.readRangeSingleMillimeters() - 14;
}



void set_height(unsigned int height)
{
  analogWrite(IN1, (int)(84.28 + 11.04*height - 0.59*height*height + 0.01*height*height*height));
}






