import cv2
import torch
import numpy as np
import platform

from flask import Flask
from flask import request
from flask import Response
from flask import Streamer
from flask import stream_with_context

"""
작물을 탐지하고 cv2 웹 스트리밍서버를 퍼블리싱하는 코드
"""

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


app = Flask(__name__)
streamer = Streamer()

@app.route('/stream')
def stream():
    src = request.args.get('src', default=0, type=int)

    try:
        return Response(
            stream_with_context(stream_gen(src)),
            mimetype='multipart/x-mixed-replace; boundary=frame')
    
    except Exception as e:
        
        print('[wandlab]', 'stream error : ',str(e))

def stream_gen(src):
    try:
        streamer.run(src)
        while True:
            frame = streamer.bytescode()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    except GeneratorExit:
        streamer.stop()










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

        results = detect_objects(model, frame)
        frame = draw_labels(results, frame)

        (grabbed, frame) = capture.read()

        if grabbed:
            cv2.imshow('Wandlab Camera Window', frame)


        cv2.imshow('video', frame)

        key = cv2.waitKey(1) & 0xFF
        if (key == 27):  # ESC 키를 누르면 종료
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

