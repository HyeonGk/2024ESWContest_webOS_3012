from flask import Flask, Response
from flask_socketio import SocketIO
import cv2
import torch
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from utils.plots import Annotator, colors
from utils.torch_utils import select_device
import time

"""
서브함수를 따로 빼서 추출한 라벨을 소켓통신하는 코드
"""

app = Flask(__name__)
socketio = SocketIO(app)

label = None  # 전역 변수 선언

@app.route('/')
def Stream():
    return Response(GenerateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def GenerateFrames():
    global label
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("Camera is not opened!")
        return -1

    weights = './best.pt'
    device = select_device('cuda:0')
    model = DetectMultiBackend(weights, device=device)
    names = model.names

    while True:
        ref, frame = cap.read()
        if not ref:
            break

        img = cv2.resize(frame, (640, 480))
        img = img[:,:,::-1].copy()  # BGR -> RGB 변환
        img = img.transpose(2,0,1)
        img = torch.from_numpy(img).to(device)
        img = img.float() / 255.0
        
        if len(img.shape) == 3:
            img = img[None]  # 배치 차원 추가

        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

        for i, det in enumerate(pred):
            annotator = Annotator(frame, line_width=3, example=str(names))
            if len(det):
                det[:, :4] = scale_boxes(img.shape[2:], det[:,:4], frame.shape).round()

                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]}'  # 글로벌 변수 업데이트
                    annotator.box_label(xyxy, label, color=colors(cls, True))
            else:
                label = None 
            frame = annotator.result()
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def send_real_label_data():
    global label
    while True:
        if label:
            print(f"Current label: {label}")  # label 값 출력
            socketio.emit('label', {'label': label})
            time.sleep(5)
        else:
            time.sleep(0.1)  # 1초마다 확인 및 전송

if __name__ == '__main__':
    # send_real_label_data를 백그라운드 태스크로 시작
    socketio.start_background_task(target=send_real_label_data)
    socketio.run(app, host='0.0.0.0', port=5000)
