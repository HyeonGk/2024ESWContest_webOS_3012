#include <AccelStepper.h>
/*
이중 컨베이어 벨트를 제어하는 코드
sketch_jul28a.ino파일을 참고함.
*/

// 저속벨트
#define dirxPin 2 
#define stepxPin 3 
#define enablePin 4

// 고속벨트
#define dirxPin2 7 
#define stepxPin2 6 
#define enablePin2 8
#define motorInterfaceType 1

AccelStepper stepperx = AccelStepper(motorInterfaceType, stepxPin, dirxPin);
AccelStepper stepperx2 = AccelStepper(motorInterfaceType, stepxPin2, dirxPin2);

void setup() {
  //저속
  pinMode(enablePin, OUTPUT);
  digitalWrite(enablePin, LOW);
  stepperx.setMaxSpeed(1500);
  stepperx.setSpeed(-1000);
  
  //고속
  pinMode(enablePin2, OUTPUT);
  digitalWrite(enablePin2, LOW);
  stepperx2.setMaxSpeed(1500);
  stepperx2.setSpeed(-5000);
}

void loop() {
  stepperx.setSpeed(-500);
  stepperx.runSpeed();
  
  stepperx2.setSpeed(-1000);
  stepperx2.runSpeed();
}
