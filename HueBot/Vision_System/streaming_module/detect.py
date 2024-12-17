import torch
import cv2
from pathlib import Path
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from utils.torch_utils import select_device
from utils.plots import Annotator, colors

# 모델 경로와 설정
weights = 'best.pt'  # YOLOv5 가중치 경로
DEVICE=''
device = select_device('cuda:0')  # CPU 사용할경우: select_device('cpu')   GPU 사용할경우: select_device('cuda:0')
model = DetectMultiBackend(weights, device=device)  # 모델 로드
stride, names = model.stride, model.names  # 모델의 stride와 클래스 이름 가져오기
imgsz = 640  # 추론 이미지 크기

# 웹캠에서 비디오 캡처
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()  # 프레임 읽기
    if not ret:
        print("웹캠에서 영상을 가져올 수 없습니다.")
        break

    # 이미지 전처리: BGR -> RGB, 사이즈 조정
    img = cv2.resize(frame, (640, 480))
    img = img[:, :, ::-1].copy()  # BGR -> RGB and HWC -> CHW로 변환하고 배열 복사
    img = img.transpose(2, 0, 1)  # HWC -> CHW
    img = torch.from_numpy(img).to(device)
    img = img.float() / 255.0  # 0-255 -> 0.0-1.0

    if len(img.shape) == 3:
        img = img[None]  # 배치 차원 추가

    # YOLOv5 추론
    pred = model(img, augment=False, visualize=False)
    #print(type(pred)) # >List 타입
    
    # NMS(Non-Maximum Suppression) 적용
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

    # 결과 처리
    for i, det in enumerate(pred):  # 탐지 결과를 각 이미지별로 처리
        annotator = Annotator(frame, line_width=3, example=str(names))  # annotator 초기화
        if len(det):
            # 탐지된 박스를 원래 프레임 크기에 맞게 스케일링
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], frame.shape).round()

            # 각 탐지에 대해 처리
            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'  # 레이블에 클래스 이름과 신뢰도 추가
                annotator.box_label(xyxy, label, color=colors(cls, True))  # 바운딩 박스 및 레이블 추가

        # 결과를 화면에 표시
        frame = annotator.result()
        cv2.imshow('YOLOv5 Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()  # 비디오 캡처 해제
cv2.destroyAllWindows()  # 모든 창 닫기
