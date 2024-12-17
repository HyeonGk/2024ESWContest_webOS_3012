import RPi.GPIO as GPIO
import serial
import time

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


while 1:
    if GPIO.input(red_apple_button_pin) == GPIO.HIGH:
        print("Red Apple!!")
        ser.write(b"R\n")
        time.sleep(0.1)
    elif GPIO.input(green_apple_button_pin) == GPIO.HIGH:
        print("Green Apple!!")
        ser.write(b"G\n")
        time.sleep(0.1)
    elif GPIO.input(decayed_apple_button_pin) == GPIO.HIGH:
        print("Decayed Apple!!")
        ser.write(b"D\n")
        time.sleep(0.1)