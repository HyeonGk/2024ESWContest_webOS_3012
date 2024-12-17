#include <AccelStepper.h>
#include <Servo.h>

Servo myservo;


// 구역별 회전에 필요한 시간(1546ms는 360도 회전)
const int R_Degrees = 258; // 120도 도달 시간
const int G_Degrees = 710;//778; // 240도 도달 시간
const int D_Degrees = 1122; // 360도 도달 시간
const int reset_Degrees = 1255; // 360도 도달 시간

int currentTime = 258; // 현재 위치를 기준으로 걸린 시간을 저장(0부터 시작)


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

  stepperx.setMaxSpeed(1000);
  stepperx2.setMaxSpeed(1800);

  Serial.println("Enter 'R', 'G', or 'D' for movement.");
}

// 목표 위치에 도달하기 위한 시간 계산 함수
int getRotationTime(int targetTime) {
  Serial.print("Target Time: ");
  Serial.print(targetTime);  // 수정된 코드
  Serial.println(" ms");

  Serial.print("Current Time: ");
  Serial.print(currentTime);  // 수정된 코드
  Serial.println(" ms");

  int rotationTime = targetTime - currentTime;

  Serial.print("Rotaion Time(before): ");
  Serial.print(rotationTime);  // 수정된 코드
  Serial.println(" ms");
  if (rotationTime < 0) {
    Serial.println("negative rotationTime");
    rotationTime += reset_Degrees; // 시계방향으로만 이동하도록 360도 더함
  }
  

  if (rotationTime > 790) {
    Serial.println("additive rotationTime");
    rotationTime += 136; // 시계방향으로만 이동하도록 360도 더함
  }

  Serial.print("Rotaion Time(after): ");
  Serial.print(rotationTime);  // 수정된 코드
  Serial.println(" ms");

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
      targetTime = R_Degrees;
      Serial.println("Moving to 120 degrees");
      break;
    case 'G':
    case 'g':
      targetTime = G_Degrees;
      Serial.println("Moving to 240 degrees");
      break;
    case 'D':
    case 'd':
      targetTime = D_Degrees;
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
    stepperx2.setSpeed(-1500);
  } else {
    stepperx.setSpeed(0);
    stepperx2.setSpeed(0);
  }

  stepperx.runSpeed();
  stepperx2.runSpeed();
}
