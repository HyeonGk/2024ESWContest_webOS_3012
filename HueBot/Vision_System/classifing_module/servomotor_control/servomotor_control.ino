#include <Servo.h>

#define servoPin 9

Servo myservo;

// 구역별 회전에 필요한 시간(1433ms는 360도 회전)
const int timeToReach120Degrees = 417; // 120도 도달 시간
const int timeToReach240Degrees = 895; // 240도 도달 시간
const int timeToReach360Degrees = 1373; // 360도 도달 시간

int currentTime = 0; // 현재 위치를 기준으로 걸린 시간을 저장(0부터 시작)

// 목표 위치에 도달하기 위한 시간 계산 함수
int getRotationTime(int targetTime) {
  int rotationTime = targetTime - currentTime;
  if (rotationTime < 0) {
    rotationTime += timeToReach360Degrees; // 시계방향으로만 이동하도록 360도 더함
  }
  return rotationTime;
}

void setup() {
  Serial.begin(9600);
  myservo.attach(servoPin); // 서보모터 핀에 연결
  myservo.write(90);  // 중립 위치로 설정 (정지 상태)
  Serial.println("Enter 'R' for the 1st zone (120 degrees), 'G' for the 2nd zone (240 degrees), or 'D' for the 3rd zone (360 degrees).");
}

void loop() {
  if (Serial.available() > 0) {
    char input = Serial.read(); // 문자 입력 받기
    int targetTime = 0;         // 목표 시간(구역별 회전시간)

    // 입력에 따라 목표 시간 설정
    switch (input) {
      case 'R':
      case 'r': // 120도 구역
        targetTime = timeToReach120Degrees;
        Serial.println("Moving to the 1st zone (120 degrees)");
        break;

      case 'G':
      case 'g': // 240도 구역
        targetTime = timeToReach240Degrees;
        Serial.println("Moving to the 2nd zone (240 degrees)");
        break;

      case 'D':
      case 'd': // 360도 구역
        targetTime = timeToReach360Degrees;
        Serial.println("Moving to the 3rd zone (360 degrees)");
        break;

      default:
        Serial.println("Invalid input. Please enter 'R', 'G', or 'D'.");
        return;
    }

    // 목표 시간까지의 회전 시간 계산
    int rotationTime = getRotationTime(targetTime);

    // 모터를 시계방향으로 회전 (회전시간에 비례하여 대기 시간 설정)
    myservo.write(0); // 시계방향 회전 시작
    delay(rotationTime); // 목표 시간만큼 대기

    // 모터 정지
    myservo.write(90); // 중립 위치로 설정하여 모터 정지

    // 현재 시간 업데이트 (다음 회전 시 기준이 됨)
    currentTime = targetTime;

    delay(500); // 다음 입력을 기다리기 전에 약간의 지연
  }
}
