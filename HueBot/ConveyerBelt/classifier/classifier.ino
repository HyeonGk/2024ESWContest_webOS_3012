import RPi.GPIO as GPIO
import time

# 사용할 GPIO 핀의 번호를 설정
red_apple_button_pin = 14  # Apple
green_apple_button_pin = 15  # Lemon
decayed_apple_button_pin = 18  # Orange

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # 핀 모드 설정 (GPIO.BCM)

# 버튼 핀의 입력 설정, PULL DOWN 설정
GPIO.setup(red_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(green_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(decayed_apple_button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def button_callback(channel):
    if channel == red_apple_button_pin:
        print("Red Apple!!")
    elif channel == green_apple_button_pin:
        print("Green Apple!!")
    elif channel == decayed_apple_button_pin:
        print("Decayed Apple!!")

# 버튼 이벤트 감지 설정
GPIO.add_event_detect(red_apple_button_pin, GPIO.RISING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(green_apple_button_pin, GPIO.RISING, callback=button_callback, bouncetime=200)
GPIO.add_event_detect(decayed_apple_button_pin, GPIO.RISING, callback=button_callback, bouncetime=200)

try:
    while True:
        time.sleep(0.1)  # 루프가 너무 빠르지 않게 조정
except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    GPIO.cleanup()