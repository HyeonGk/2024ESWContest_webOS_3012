#include <AFMotor.h>
#include <SoftwareSerial.h>

// 블루투스 모듈과 연결된 핀 설정
int Tx = 9; //리눅스: 9  윈도우: 0
int Rx = 10; //리눅스: 10 윈도우: 1
SoftwareSerial mySerial(Tx, Rx); // RX, TX

// 1번과 4번 모터 제어 객체 생성
AF_DCMotor motor1(1);
AF_DCMotor motor4(4);

int sp = 150;  // 기본 모터 속도 설정

void setup() {
  // 시리얼 통신과 블루투스 통신 초기화
  Serial.begin(9600);
  mySerial.begin(9600);

  // 모터 초기화 및 정지 상태 설정
  motor1.setSpeed(sp);
  motor1.run(RELEASE);  // 정지

  motor4.setSpeed(sp);
  motor4.run(RELEASE);  // 정지

  Serial.println("Ready for Bluetooth commands...");
}

void loop() {
  if (mySerial.available()) {
    char command = mySerial.read();  // 한 글자씩 읽기
    Serial.println("Received command: " + String(command));
    
    handleCommand(command);  // 명령을 처리하는 함수 호출
  }
  delay(10);  // 약간의 대기 (CPU 과부하 방지)
}

// 명령을 처리하는 함수
void handleCommand(char cmd) {
  if (cmd == '1') {  // 정지 명령
    Serial.println("Stopping motors...");
    motor1.setSpeed(0);
    motor4.setSpeed(0);
    motor1.run(RELEASE);  // 모터 정지
    motor4.run(RELEASE);
  } 
  else if (cmd == '2') {  // 작동 명령
    Serial.println("Starting motors...");
    motor1.setSpeed(sp);
    motor4.setSpeed(sp);
    motor1.run(FORWARD);  // 모터 전진
    motor4.run(FORWARD);
  } 
  else {
    Serial.println("Unknown command received.");
  }
}
