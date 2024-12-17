import cv2
import time
import copy

"""
OpenCV를 사용하여 초당 한 장씩 총 10장의 사진을 찍는 매크로 코드
"""

# 카메라 초기화
cap = cv2.VideoCapture(1)
time.sleep(1)

#-- 웹캠 오류 처리 
# if not cap.isOpened():
#     print("WebCam is not running")
#     exit()

alpha = 1
omega = 10


# 사진 촬영
for i in range(alpha,omega+1):
    ret, frame = cap.read()  # 카메라에서 프레임 읽기

    # 이미지 깊은복사
    converted_frame = copy.deepcopy(frame)
    # 이미지 명암조절
    contrast_image = cv2.convertScaleAbs(converted_frame, alpha=1.4)
    
    cv2.imshow('Webcam', contrast_image)
    
    # 프레임 저장
    cv2.imwrite(f"./images/image_{i + 1}.jpg", frame)
    print(f"Image {i + 1} captured.")
    
    # 1.5초 대기
    time.sleep(1.5)

    # 1초 대기
    time.sleep(1.5)


# 카메라 해제
cap.release()
cv2.destroyAllWindows()
