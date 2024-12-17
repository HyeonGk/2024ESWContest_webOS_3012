import cv2
import torch
import numpy as np
import copy
# import RPi.GPIO as GPIO
import serial
import time

"""
단순히 작물을 탐지해서 cv2 윈도우에 띄우는 코드
"""

# 시리얼 통신 설정
#ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
#ser.flush()

# GPIO 연결 설정
# GPIO.setwarnings(False)
# GPIO.setmode(GPIO.BCM) #핀모드 설정(GPIO.BCM/GPIO.BOARD)

def load_yolov5():
    # YOLOv5 모델 로드
    #model = torch.hub.load('ultralytics/yolov5', 'yolov5s', trust_repo=True)  # yolov5s, yolov5m, yolov5l, yolov5x 중 선택 가능
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='./../models/best.pt')
    return model

def detect_objects(model, frame):
    # 객체 탐지 수행
    results = model(frame)
    return results

def draw_labels(results, frame):
    labels, cords = results.xyxyn[0][:, -1].cpu().numpy(), results.xyxyn[0][:, :-1].cpu().numpy()
    
    # label[1]: apple
    # label[2]: orange
    # label[3]: lemon
    #print(f"labels: {labels}")
    if len(labels) > 0:
        if labels[0] == 1:
            print("Apple!!")
        elif labels[0] == 2:
            print("Orange!!")
        elif labels[0] == 3:
            print("Lemon!!")
         
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    for i in range(n):
        row = cords[i]
        if row[4] >= 0.5:  # confidence threshold
            x1, y1, x2, y2 = int(row[0] * x_shape), int(row[1] * y_shape), int(row[2] * x_shape), int(row[3] * y_shape)
            bgr = (0, 255, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), bgr, 2)
            cv2.putText(frame, f'{results.names[int(labels[i])]} {row[4]:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

    return frame

def main():
    #cap = cv2.VideoCapture("http://192.168.117.229:8080/?action=stream")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return -1

    model = load_yolov5()

    while True:
        ret, frame = cap.read()
        if not ret:
            break


        converted_frame = copy.deepcopy(frame)

        # 명암 조절
        alpha = 1.5
        contrast_image = cv2.convertScaleAbs(converted_frame, alpha=alpha)


        # 밝기 조절 (예시: 50만큼 밝게)
        #brightness = 0
        #bright_image = cv2.add(converted_frame, np.ones(converted_frame.shape, dtype=np.uint8) * brightness)

        results = detect_objects(model, contrast_image)
        frame = draw_labels(results, contrast_image)

        cv2.imshow('video', frame)
        if cv2.waitKey(1) == 27:  # ESC 키를 누르면 종료
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

