#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>

#define DHTPIN 16   // DHT 센서 데이터 핀
#define DHTTYPE DHT11  // 사용 중인 DHT 센서 유형 (DHT11)
#define WIFI_SSID "jacksmith"  // WiFi SSID
#define WIFI_PASSWORD "12345678"  // WiFi 비밀번호
#define SERVER_URL "http://192.168.242.90:3000/esp32"  // 서버 주소

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();  // DHT 센서 초기화

  // WiFi 연결 설정
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi....");
  }
  Serial.println("Connected to WiFi");

  // ESP32 IP 주소 출력
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  delay(2000);  // DHT 센서 안정화 시간 필요 (약 2초)

  // 온도와 습도 읽기
  float tem = dht.readTemperature();
  float hum = dht.readHumidity();
  
  // 온도 또는 습도 읽기 실패 시 에러 메시지 출력
  if (isnan(tem) || isnan(hum)) {
    Serial.println("센서로부터 데이터를 읽을 수 없습니다.");
    return;
  }

  // 온도와 습도 출력
  Serial.print("Temperature : ");
  Serial.print(tem);
  Serial.println("C");

  Serial.print("Humidity : ");
  Serial.print(hum);
  Serial.println("%");

  // 서버로 데이터 전송
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    http.begin(SERVER_URL);  // 서버 URL 설정
    http.addHeader("Content-Type", "application/json");  // 헤더 설정

    // JSON 형식으로 데이터 전송
    String payload = "{\"temperature\":" + String(tem) + ", \"humidity\":" + String(hum) + "}";
    int httpResponseCode = http.POST(payload);  // POST 요청 전송

    if (httpResponseCode > 0) {
      Serial.print("ESP32 IP Address: ");
      Serial.println(WiFi.localIP());
      Serial.print("서버 응답 코드: ");
      Serial.println(httpResponseCode);  // 서버 응답 출력
    } else {
      Serial.print("ESP32 IP Address: ");
      Serial.println(WiFi.localIP());
      Serial.print("POST 요청 실패, 에러: ");
      Serial.println(http.errorToString(httpResponseCode).c_str());
    }

    http.end();  // 연결 종료
  } else {
    Serial.println("WiFi 연결 실패");
  }
}