#include <AccelStepper.h>
#include <Servo.h>

Servo myservo;

// 회전 시간 설정
const int timeToReach120Degrees = 417;
const int timeToReach240Degrees = 895;
const int timeToReach360Degrees = 1373;

int currentTime = 0;  // 현재 위치 기준 시간

// 모터 핀 설정
#define dirxPin 2
#define stepxPin 3
#define enablePin 4

#define dirxPin2 7
#define stepxPin2 6
#define enablePin2 8
#define motorInterfaceType 1

AccelStepper stepperx(motorInterfaceType, stepxPin, dirxPin);
AccelStepper stepperx2(motorInterfaceType, stepxPin2, dirxPin2);

bool beltActive = true;  // 벨트 활성화 상태 관리

void setup() {
  Serial.begin(9600);
  myservo.attach(9);  
  myservo.write(90);  // 서보 모터 중립 위치 설정

  pinMode(enablePin, OUTPUT);
  pinMode(enablePin2, OUTPUT);

  digitalWrite(enablePin, LOW);
  digitalWrite(enablePin2, LOW);

  stepperx.setMaxSpeed(1800);
  stepperx2.setMaxSpeed(1000);

  Serial.println("Enter 'R', 'G', or 'D' for movement.");
}

int getRotationTime(int targetTime) {
  int rotationTime = targetTime - currentTime;
  if (rotationTime < 0) {
    rotationTime += timeToReach360Degrees;  // 시계방향 회전
  }
  return rotationTime;
}

void activateBelt() {
  beltActive = true;
}

void deactivateBelt() {
  beltActive = false;
}

void processInput(char input) {
  deactivateBelt();  // 벨트 멈추기

  int targetTime = 0;
  switch (input) {
    case 'R':
    case 'r':
      targetTime = timeToReach120Degrees;
      Serial.println("Moving to 120 degrees");
      break;
    case 'G':
    case 'g':
      targetTime = timeToReach240Degrees;
      Serial.println("Moving to 240 degrees");
      break;
    case 'D':
    case 'd':
      targetTime = timeToReach360Degrees;
      Serial.println("Moving to 360 degrees");
      break;
    default:
      Serial.println("Invalid input.");
      return;
  }

  int rotationTime = getRotationTime(targetTime);
  myservo.write(0);  // 회전 시작
  delay(rotationTime);  // 목표 시간까지 대기
  myservo.write(90);  // 중립 위치로 복귀

  currentTime = targetTime;  // 시간 갱신

  delay(500);  // 짧은 대기 시간
  activateBelt();  // 벨트 재가동
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read();
    processInput(input);
  }
  beltActive = true;
  if (beltActive) {
    stepperx.setSpeed(-500);
    stepperx2.setSpeed(-1000);
  } else {
    stepperx.setSpeed(0);
    stepperx2.setSpeed(0);
  }

  stepperx.runSpeed();
  stepperx2.runSpeed();
}
