const int redAppleLED = 3;    // 빨간 사과에 해당하는 LED 핀
const int greenAppleLED = 4;  // 녹색 사과에 해당하는 LED 핀
const int decayedAppleLED = 5; // 썩은 사과에 해당하는 LED 핀

"""
라즈베리파이에서 아두이노로 시리얼통신이 제대로 보내지는지 확인하는 코드
"""

void setup() {
  // LED 핀을 출력으로 설정
  pinMode(redAppleLED, OUTPUT);
  pinMode(greenAppleLED, OUTPUT);
  pinMode(decayedAppleLED, OUTPUT);

  // 시리얼 통신 시작 (9600 baud rate로 설정)
  Serial.begin(9600);
  Serial.println("Arduino is ready to receive data.");
}

void loop() {
  // 시리얼 데이터가 수신되었는지 확인
  if (Serial.available() > 0) {
    char receivedData = Serial.read(); // 수신된 데이터를 읽음

    // 수신된 문자에 따라 동작 수행
    switch (receivedData) {
      case 'R':  // 빨간 사과 처리
        Serial.println("Red Apple detected!");
        digitalWrite(redAppleLED, HIGH);  // 빨간 LED 켜기
        delay(3000);  // 3초 대기
        digitalWrite(redAppleLED, LOW);   // LED 끄기
        break;

      case 'G':  // 녹색 사과 처리
        Serial.println("Green Apple detected!");
        digitalWrite(greenAppleLED, HIGH);  // 녹색 LED 켜기
        delay(3000);  // 3초 대기
        digitalWrite(greenAppleLED, LOW);   // LED 끄기
        break;

      case 'D':  // 썩은 사과 처리
        Serial.println("Decayed Apple detected!");
        digitalWrite(decayedAppleLED, HIGH);  // 썩은 사과 LED 켜기
        delay(3000);  // 3초 대기
        digitalWrite(decayedAppleLED, LOW);   // LED 끄기
        break;

      default:  // 알 수 없는 데이터 처리
        Serial.println("Unknown command received.");
        break;
    }
  }
}
