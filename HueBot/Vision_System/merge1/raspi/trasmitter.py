"""
transmitter.py코드를 참고하여 flask위에서 사물식별을 진행하고, 이때 사물이 식별되면 따로 브랜치 콜백에 들어가서 
분류기를 회전시키고 1초 동안 컨베이어벨트를 움직이는 작업을 진행하도록 함.
(즉, PC에서 받은 AI정보를 그대로 아두이노 전달하기 위한 브릿지 역할)
"""
import socketio
import keyboard
import time
import RPi.GPIO as GPIO
import serial

# 사용할 GPIO핀의 번호를 설정
red_apple_button_pin = 14 # red_apple
green_apple_button_pin = 15 # green_apple
decayed_apple_button_pin = 18 # decayed_apple

# 시리얼 통신 설정
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.flush()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) #핀모드 설정(GPIO.BCM/GPIO.BOARD)

# 버튼 핀의 입력설정, PULL DOWN 설정(입출력 초기화하는 코드인듯)
GPIO.setup(red_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(green_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(decayed_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


# Flask 서버에 연결하기 위해 SocketIO 클라이언트 인스턴스 생성
sio = socketio.Client()

# 서버에 연결되었을때 호출되는 이벤트 헨들러
@sio.event
def connect():
    print('Connected to the server')

# 서버와 연결이 끊어졌을떄 호추되는 이벤트 헨들러
@sio.event
def disconnect():
    print('Disconnected from the server')

# 서버로부터 'real_time_text' 이벤트를 수신했을때 호출되는 이벤트 헨들러
@sio.on('label')
def handle_real_time_text(data):
    #print(f"Received data: {data['label']}")
    if data['label'] == 'red':
        print("Red Apple!!")
        ser.write(b"R\n")
        time.sleep(3)
    elif data['label'] == 'green':
        print("Green Apple!!")
        ser.write(b"G\n")
        time.sleep(3)
    elif data['label'] == 'decay':
        print("Decayed Apple!!")
        ser.write(b"D\n")
        time.sleep(3)


# 키보드에 인터럽트 거는 기능 넣어주기(ctrl+c)
try:
    # 서버에 연결 시도
    sio.connect('http://192.168.145.158:5000')

    # 분류기 보정을 위한 수동조작 모드
    while True:
        time.sleep(0.1)  # CPU 사용량을 줄이기 위해 약간의 대기 시간을 둠
        
        if GPIO.input(red_apple_button_pin) == GPIO.HIGH:
            print("Red Apple!!")
            ser.write(b"R\n")
            time.sleep(3)
        elif GPIO.input(green_apple_button_pin) == GPIO.HIGH:
            print("Green Apple!!")
            ser.write(b"G\n")
            time.sleep(3)
        elif GPIO.input(decayed_apple_button_pin) == GPIO.HIGH:
            print("Decayed Apple!!")
            ser.write(b"D\n")
            time.sleep(3)

except KeyboardInterrupt:
    print("\nProgram interrupted. Closing connection...")
    sio.disconnect()  # 소켓 연결 종료
    print("Connection closed.")